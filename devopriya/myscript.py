def llm_langchain(string):
    import requests 
    import json
    url = "http://localhost:11434/api/generate"
    headers = {
        "Content-Type":"application/json"
    }
    
    data = {
        "model" : "llama2-uncensored",
        "prompt": string + " Provide the subject for this.",
        "stream": False
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        response_text = response.text
        data  = json.loads(response_text)
        actual_response = data["response"]
        #print("actual_response : ", actual_response)
        return actual_response
    
    else:
        print("error: ", response.status_code, response.text)

import mysql.connector as cnctr


connx = cnctr.connect(host='db-mysql-blr1-82262-do-user-13433417-0.i.db.ondigitalocean.com',port='25060', username='doadmin', password='AVNS_8JrUC6kgyaIWXPq5GNC', database='defaultdb')
crsr = connx.cursor()

connxn = cnctr.connect(host='db-mysql-blr1-82262-do-user-13433417-0.i.db.ondigitalocean.com',port='25060', username='doadmin', password='AVNS_8JrUC6kgyaIWXPq5GNC', database='defaultdb')

  
insert_crsr = connxn.cursor(buffered=True)

#print("Connection is successful!!!")

operation = "select categories, sub_categories, prompt from response_for_chatbot where ingestion_time = (select max(ingestion_time) from response_for_chatbot)"

schema = ['categories', 'sub categories', 'prompt']


crsr.execute(operation)
for row in crsr:
  lis = []
  string = ''
  ln_arr =[]
  for i, ln in zip(row, range(len(row))):
    ln_arr.append(ln)
    lis.append(i)
    if i is None:
      string += ''
    else:
      if schema[ln] == "categories":
        string += "The email which is to be sent is of a " + i + ' '
      if schema[ln] == "sub categories":
        string += ". This should be an " + i + ' '
      if schema[ln] == "prompt":
        string += ". The email prompt is " + i + ' '

  #print(str)

string += " Don't add the subject part to this output."


if 'COLLEGE' in string.upper():
  tablename = "students"

#operation = "select distinct `Company Email Id` from {tablename}".format(tablename=tablename)

'''
for result in crsr.execute(operation, multi=True):
  if result.with_rows:
    #print("Rows produced by statement '{}':".format(
      #result.statement))
    arr = (result.fetchall())
  else:
    print("Number of rows affected by statement '{}': {}".format(
      result.statement, result.rowcount))
'''

schema = ['Employee ID','Employee Name','Indian Phone Number','Company Email ID','Personal Email ID','Father\'s Name','Mother\'s Name','Sibling Name','Reporting Boss Name',
'Ongoing Projects','Hobbies','Date of Birth','Recent Official Visits','Leaves Availed','Leaves Remaining','Education Qualification','Institute','Type of Mobile Phone (Official)',
'Type of Mobile Phone (Personal)']
crsr.execute("select * from {tablename} limit 3".format(tablename=tablename))
counter = 0

for row in crsr:
  lis = []
  inp = ''
  ln_arr =[]
  for i, ln in zip(row, range(len(row))):
    ln_arr.append(ln)
    lis.append(i)
    if i is None:
      inp += ''
    else:
      if schema[ln] == 'Company Email ID':
        to = i
        
    inp += schema[ln] + ' is '+ i + '. '
    frm = "test@example.com"

  

  #message = "test"
  #subject = "test"
  subject = llm_langchain(string + " Provide the subject for this.")
  message = llm_langchain(inp + string + "Only provide the email body. Don't provide the subject.")
  
  ins_operation = "insert into response_from_chatbot values ('{to}', '{frm}', '{subject}', '{message}');".format(to=to, frm=frm, subject=subject.replace('"', '').replace("'", ""), message=message.replace('"', '').replace("'", ""))
  
  
  #print("operation is -> ", ins_operation)
  
  
  
  insert_crsr.execute(ins_operation)
  connxn.commit()
  
  counter += 1
  #print("Total rows inserted : ", counter)



#for i in arr:
  

connx.commit()
connx.close()
connxn.close()
#llm_langchain(str)
