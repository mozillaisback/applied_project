import os
from time import sleep
import sys
import socket
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP, AES
from Crypto.Signature import pkcs1_15, PKCS1_v1_5 
from Crypto.Hash import SHA256
from base64 import b64encode, b64decode


def exec_shell_cmd(cmd):
    import subprocess
    subprocess.Popen(cmd, shell=True)
    return 0




def generate_server_keys():

#    exec_shell_cmd('pwd')
    path = os.getcwd() + '/'
    if os.path.exists(path + 'server_private_key.pem'):
        pass
    else:
        exec_shell_cmd('openssl genrsa -out {path}server_private_key.pem 2048'.format(path=path))
        sleep(10)
        #This command generates a 2048-bit RSA private key in the file `server_private_key.pem`.

        #To generate a public key from the private key:
        exec_shell_cmd('openssl rsa -pubout -in {path}server_private_key.pem -out server_public_key.pem'.format(path=path))
        sleep(10)
    #This command generates the corresponding public key and saves it in the file `server_public_key.pem`.
    return 0



def start_server():
# Load server RSA keys generated with OpenSSL
    with open("/home/nothing/wans/server_private_key.pem", "rb") as key_file:
        server_private_key = RSA.import_key(key_file.read())

    with open("/home/nothing/wans/server_public_key.pem", "rb") as key_file:
        server_public_key = RSA.import_key(key_file.read())

    print("\nServer's public key is : ", server_public_key)
    print("\nServer's private key is : ", server_private_key) 
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 65432))
    server_socket.listen(1)
    print("Server is listening...")

    conn, addr = server_socket.accept()
    print(f"Connected by {addr}")

    # Send server's public key to the client
    conn.sendall(server_public_key.export_key())
    print("\nPublic key has been sent to client!!!!")

    # Receive client's public key
    client_public_key = RSA.import_key(conn.recv(4096))
#    print("Size of Client public key is : ", sys.getsizeof(client_public_key))
    
    # Receive the encrypted AES key from the client
    encrypted_session_key = conn.recv(256)
#    print("\nEncrypted session key is of ", sys.getsizeof(encrypted_session_key), " bytes!!!!")
#    print("encrypted session key is : ", encrypted_session_key)
    cipher_rsa = PKCS1_OAEP.new(server_private_key)
    session_key = cipher_rsa.decrypt(encrypted_session_key)
    print("Session key received and decrypted.")

    # Now, let's receive an encrypted and signed message from the client
    encrypted_message = conn.recv(40)
#    print("\nEncrypted message is of ", sys.getsizeof(encrypted_message), " bytes!!!!")
    signature = conn.recv(256)
#    print("\nSignature is of ", sys.getsizeof(signature), " bytes!!!!")
#    print("\nEncrypted Message received is : ", encrypted_message)
#    print("\nSignature is : ", signature)

    # Decrypt the message using the session key
    nonce = encrypted_message[:16]
    cipher_aes = AES.new(session_key, AES.MODE_EAX, nonce=nonce)
    decrypted_message = cipher_aes.decrypt(encrypted_message[16:])
    
    # Verify the signature using the client's public key
    h = SHA256.new(decrypted_message)
    #print(h)
    try:
#        print("hash value : ", h)
#        print("Ran here fine !!!!")
#       print(pkcs1_15.new(client_public_key))
        pkcs1_15.new(client_public_key).verify(h, signature)
#        print("Ran here fine post ver !!!!")
        print("Signature verified.")
        print(f"Decrypted message: {decrypted_message.decode('utf-8')}")
    except (ValueError, TypeError):
        print("Signature verification failed.")

    conn.close()
    server_socket.close()

if __name__ == "__main__":
    generate_server_keys()
    start_server()
