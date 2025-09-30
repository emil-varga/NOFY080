from multiprocessing.connection import Client

# This assumes that instrument_server.py from example code
# is running on the IP address and port below with the password
# 'password' and that the Pico is connected to the remote computer
IP_ADDRESS = "<IP_ADDRESS>"
PORT = <PORT>

#here b'' means a bytestring
#Strings in Python are by default unicode, this will force
#the string to consist of individual bytes (like in C or Pascal),
#which is a requirement for the Client/Listener passwords
password = b'<PASSWORD>'

#open the connection
address = (IP_ADDRESS, PORT)
with Client(address, authkey=password) as conn:
    #and start talking to the server
    conn.send(":READ:T?")
    resp = conn.recv()
    # We are using TCP/IP, so we have to 
    # receive the response, even if we discard it
    conn.send(":LED 2 1")
    conn.recv()
    print("Response :", resp)