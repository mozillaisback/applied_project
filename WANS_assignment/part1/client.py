import os
from time import sleep
import sys
import socket
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP, AES
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from base64 import b64encode, b64decode


def exec_shell_cmd(cmd):
    import subprocess
    output = subprocess.Popen(cmd, shell=True)
    return output



def generate_client_keys():

#    exec_shell_cmd('pwd')
    path = os.getcwd() + "/"
    if os.path.exists('{path}client_private_key.pem'.format(path=path)):
        pass
    else:
        exec_shell_cmd('openssl genrsa -out {path}client_private_key.pem 2048'.format(path=path))
        #This command generates a 2048-bit RSA private key in the file `client_private_key.pem`.
        sleep(10)

        #To generate a public key from the private key:
    
        exec_shell_cmd('openssl rsa -pubout -in {path}client_private_key.pem -out {path}client_public_key.pem'.format(path=path))
        sleep(10)
    
        #This command generates the corresponding public key and saves it in the file `client_public_key.pem`.
    return 0



def start_client():
# Load client RSA keys generated with OpenSSL
    with open("client_private_key.pem", "rb") as key_file:
        client_private_key = RSA.import_key(key_file.read())

    with open("client_public_key.pem", "rb") as key_file:
        client_public_key = RSA.import_key(key_file.read())

    print("\nClient's public key is : ", client_public_key)
    print("\nClient's public key is : ", client_private_key)
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 65432))

    # Receive server's public key
    server_public_key = RSA.import_key(client_socket.recv(4096))
    
    # Send client's public key to the server
    client_socket.sendall(client_public_key.export_key())
#    print("\nPublic key is of ", sys.getsizeof(client_public_key), " bytes!!!!")
    print("\nPublic key has been sent to server!!!!")
    
    # Generate AES session key
    session_key = os.urandom(16)
    
    # Encrypt the session key with the server's public key
    cipher_rsa = PKCS1_OAEP.new(server_public_key)
    encrypted_session_key = cipher_rsa.encrypt(session_key)
#    print("\nEncrypted session key is of ", sys.getsizeof(encrypted_session_key), " bytes!!!!")
    client_socket.sendall(encrypted_session_key)
    print("\nSession key sent!!!!")

    # Now, let's send an encrypted and signed message to the server
    message = "This is a secret message"
    
    # Encrypt the message using the session key
    cipher_aes = AES.new(session_key, AES.MODE_EAX)
    ciphertext, tag = cipher_aes.encrypt_and_digest(message.encode('utf-8'))
    encrypted_message = cipher_aes.nonce + ciphertext
    

    #sending encrypted message
    client_socket.sendall(encrypted_message)
#    print("\nEncrypted message is of ", sys.getsizeof(encrypted_message), " bytes!!!!")
    # Sign the message
    h = SHA256.new(message.encode('utf-8'))
    signature = pkcs1_15.new(client_private_key).sign(h)
#    print(sys.getsizeof(signature))
#    print("Signature is : ", signature)
    
    # Send the encrypted message and the signature to the server
    #client_socket.sendall(encrypted_message)
    client_socket.sendall(signature)
#    print("\nSignature is of ", sys.getsizeof(signature), " bytes!!!!")
    print("\nSignature has been sent!!!!")
    
    client_socket.close()

if __name__ == "__main__":
    generate_client_keys()
    start_client()
