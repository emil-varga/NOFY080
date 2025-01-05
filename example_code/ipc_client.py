import numpy as np
from multiprocessing.connection import Client

address = ('localhost', 6000)
passowrd = b'password'
with Client(address, authkey=passowrd) as conn:
    # send and recv pickle and unpickle, respectively
    # the objects we try to send. So we can send essentially
    # arbitrary data
    conn.send({'key1': 'hello', 'key2': np.arange(5)})
    resp = conn.recv()
    print("Response :", resp)