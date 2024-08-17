## Importing the basic libraries
import os
from time import sleep
import sys
import socket
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP, AES
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from base64 import b64encode, b64decode




## Function which performs the client side function
def start_client():
    from clien_side_key_exchange import client_side_exchange
    server_public_key, client_private_key = client_side_exchange()

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    client_socket.connect(('localhost', 11564))



    client_hello = 'HELLO!!!!'
    encode_client_hello = client_hello.encode("utf-8")
    client_socket.sendall(encode_client_hello)
    print("\n")

    server_ackn = client_socket.recv(40)
    decode_server_ackn = server_ackn.decode("utf-8")
    print("\n\n",decode_server_ackn)



    client_ack = "ACK!!!!"
    encode_client_ack = client_ack.encode("utf-8")
    client_socket.sendall(encode_client_ack)
    print("\n")

    
    
    
    # Generate AES session key
    session_key = os.urandom(16)
    
    # Encrypt the session key with the server's public key
    cipher_rsa = PKCS1_OAEP.new(server_public_key)
    encrypted_session_key = cipher_rsa.encrypt(session_key)

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

    # Sign the message
    h = SHA256.new(message.encode('utf-8'))
    signature = pkcs1_15.new(client_private_key).sign(h)
    
    # Send the encrypted message and the signature to the server
    client_socket.sendall(signature)
    print("\nSignature has been sent!!!!")

    
    
    client_close = "CLOSE!!!!"
    client_socket.sendall(client_close.encode("utf-8"))
    print("\n")
     
    client_socket.close()
    del client_socket
    exit(0)

if __name__ == "__main__":
    start_client()
