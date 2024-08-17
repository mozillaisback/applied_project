## Loading the basic libraries
import os
from time import sleep
import sys
import socket
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP, AES
from Crypto.Signature import pkcs1_15, PKCS1_v1_5 
from Crypto.Hash import SHA256
from base64 import b64encode, b64decode

## Creating a function to run the shell commands
def exec_shell_cmd(cmd):
    import subprocess
    subprocess.Popen(cmd, shell=True)
    return 0


## START SERVER Function this consists of server side operations that is performed
def start_server():

    from server_side_key_exchange import server_key_exchange

    client_public_key, server_private_key = server_key_exchange()

    # SOCKET CREATION
    # Port 11564 is used to run the server socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('localhost', 11564))
    server_socket.listen(2)
    conn, addr = server_socket.accept()



    ## RECEIVING CLIENT HELLO
    client_hello = conn.recv(256)
    decode_client_hello = client_hello.decode("utf-8")
    print("\n\n", decode_client_hello)

    ## SENDING HELLO + ACK TO CLIENT
    server_ackn = "Hello+Ack!!!!"
    conn.sendall(server_ackn.encode("utf-8"))
    print("\n")

    ## RECEIVING CLIENT ACK
    client_ack =  conn.recv(256)
    decode_client_ack = client_ack.decode("utf-8")
    print("\n\n", decode_client_ack)

    


    
    # Receive the encrypted AES key from the client
    encrypted_session_key = conn.recv(256)
    print("\n")
    cipher_rsa = PKCS1_OAEP.new(server_private_key)
    session_key = cipher_rsa.decrypt(encrypted_session_key)
    print("\nSession key received and decrypted.")

    # Now, let's receive an encrypted and signed message from the client
    encrypted_message = conn.recv(40)
    print("\n")

    signature = conn.recv(256)
    print("\n")

    # Decrypt the message using the session key
    nonce = encrypted_message[:16]
    cipher_aes = AES.new(session_key, AES.MODE_EAX, nonce=nonce)
    decrypted_message = cipher_aes.decrypt(encrypted_message[16:])
    
    # Verify the signature using the client's public key
    h = SHA256.new(decrypted_message)
    #print(h)
    try:
        pkcs1_15.new(client_public_key).verify(h, signature)

        print("Signature verified.")
        print(f"Decrypted message: {decrypted_message.decode('utf-8')}")
    except (ValueError, TypeError):
        print("Signature verification failed.")

    client_close = conn.recv(40)
    decode_client_close = client_close.decode("utf-8")
    print("\n\n", decode_client_close)

    conn.close()
    server_socket.close()
    
    del conn
    del server_socket
    return 0 

if __name__ == "__main__":

    start_server()
