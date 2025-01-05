from multiprocessing.connection import Client

address = ('nt202', 34317)
password = b'NOFY080_2024'
with Client(address, authkey=password) as conn:
    conn.send(':LED 3 1')
    resp = conn.recv()
    print("Response :", resp)
