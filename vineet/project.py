from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from threading import Thread
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import pandas as pd
import re
import requests

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with your actual secret key

# Email configuration parameters for Zoho Mail
email_config = {
    'smtp_server': 'smtp.zoho.com',  # Zoho SMTP server
    'smtp_port': 587,  # TLS port for Zoho
}

# A dictionary to store user data for simplicity. In production, this should be a database.
user_data = {}

# Function to fetch email data from an Excel file
def fetch_email_data_from_excel(file_path):
    df = pd.read_excel(file_path)
    return df

# Function to check if the content is HTML or plain text
def is_html(content):
    return bool(re.search(r'<[a-z][\s\S]*>', content, re.IGNORECASE))

# Function to get the client's IP address
def get_client_ip():
    if request.headers.get('X-Forwarded-For'):
        ip = request.headers.get('X-Forwarded-For').split(',')[0]
    elif request.headers.get('X-Real-IP'):
        ip = request.headers.get('X-Real-IP')
    else:
        ip = request.remote_addr
    return ip

# Send email function
def send_email(recipient_email, subject, body_header, body, email_user, email_password, from_email):
    # Create the email
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = recipient_email
    msg['Subject'] = subject
    
    # Combine body header with the body
    if not is_html(body):
        # If the body is plain text, convert it to basic HTML
        body = f"<p>{body.replace('\n', '<br>')}</p>"
    
    # Create a tracking link
    tracking_link = f"http://localhost:5000/track?email={recipient_email}"
    
    # Append the tracking link to the email body
    full_body = f"{body_header}<br><br>{body}<br><br><a href='{tracking_link}'>Click here to confirm your email</a>"
    
    # Attach the body of the email (HTML format to support hyperlinks)
    msg.attach(MIMEText(full_body, 'html'))
    
    # Use a context manager to manage the SMTP connection
    try:
        with smtplib.SMTP(email_config['smtp_server'], email_config['smtp_port']) as server:
            server.starttls()
            server.login(email_user, email_password)
            server.send_message(msg)
            print(f"Email successfully sent to {recipient_email}.")
    except smtplib.SMTPAuthenticationError as e:
        print(f"Failed to authenticate: {e}")
        flash(f"Failed to authenticate: {e}")
    except Exception as e:
        print(f"Failed to send email to {recipient_email}: {e}")

# Background task to send emails
def send_emails(file_path, email_user, email_password, from_email):
    email_data_df = fetch_email_data_from_excel(file_path)
    
    # Loop through each row in the email data DataFrame and send an email
    for index, row in email_data_df.iterrows():
        recipient_email = row['To']
        subject = row['Subject']
        body_header = row.get('Body Header', '')  # Get the Body Header, default to empty string if not present
        body = row['Body']  # Body can include plain text or HTML
        
        try:
            print(f"Sending email to {recipient_email}...")  # Debugging output
            send_email(recipient_email, subject, body_header, body, email_user, email_password, from_email)
        except Exception as e:
            print(f"Failed to send email to {recipient_email}: {e}")
            continue  # Continue to the next email if an error occurs

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_emails', methods=['POST'])
def handle_send_emails():
    email_user = request.form['email_user']
    email_password = request.form['email_password']
    from_email = request.form['from_email']
    
    if 'file_path' not in request.files:
        flash("No file part")
        return redirect(request.url)
    
    file = request.files['file_path']
    
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    
    file_path = file.filename
    file.save(file_path)
    
    thread = Thread(target=send_emails, args=(file_path, email_user, email_password, from_email))
    thread.start()
    
    flash("Emails are being sent in the background!")
    return redirect(url_for('index'))

@app.route('/track', methods=['GET'])
def track_user():
    email = request.args.get('email')
    ip_address = get_client_ip()
    
    geo_info = requests.get(f'http://ipinfo.io/{ip_address}/json').json()
    
    user_data[email] = {
        'ip_address': ip_address,
        'geo_info': geo_info
    }
    
    return render_template('thank_you.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', user_data=user_data)

@app.route('/fetch_user_data')
def fetch_user_data():
    # Return JSON data for the dashboard
    return jsonify(user_data)

if __name__ == "__main__":
    app.run(debug=True)
