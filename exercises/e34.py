from multiprocessing.connection import Client

# This assumes that instrument_server.py from example code
# is running on the IP address and port below with the password
# 'password' and that the Pico is connected to the remote computer
IP_ADDRESS = "195.113.24.159"
PORT = 34317

#here b'' means a bytestring
#Strings in Python are by default unicode, this will force
#the string to consist of individual bytes (like in C or Pascal),
#which is a requirement for the Client/Listener passwords
passowrd = b'NOFY080_2024'

#open the connection
address = (IP_ADDRESS, PORT)
with Client(address, authkey=passowrd) as conn:
    #and start talking to the server
    conn.send(":READ:T?")
    resp = conn.recv()
    # We are using TCP/IP, so we have to 
    # receive the response, even if we discard it
    conn.send(":LED 2 1")
    conn.recv()
    print("Response :", resp)