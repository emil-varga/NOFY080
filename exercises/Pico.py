# exercises 30 and 31

import pyvisa as vi
import numpy as np

class Pico:
    def __init__(self, rm, addr=None):
        if addr is None:
            # if the address is not specified
            # obtain a list of all addresses and try them all
            addrs = rm.list_resources()
            for _addr in addrs:
                try:
                    # the attempt can fail at two points: opening the port or attempt at acommunication
                    # we need to disinguish the two, because if exception occured in open_resource()
                    # we shouldn't close the session, but if the problem is in communication we should
                    # close the session
                    opened=False
                    self.dev = rm.open_resource(_addr, write_termination='\n', read_termination='\n')
                    opened=True
                    resp = self.dev.query('*IDN?')
                    if resp.strip() == 'PICO':
                        break
                    else:
                        # it replied something we don't expect
                        self.dev.close() 
                except Exception as e:
                    # print(e)
                    if opened:
                        self.dev.close()
        else:
            # of the address was specified just open the session and return that
            _addr = addr
            self.dev = rm.open_resource(_addr,
                                        write_termination='\n',
                                        read_termination='\n')
        print(self.dev.query('*IDN?'))
    
    def idn(self):
        return self.dev.query('*IDN?')

    def led(self, n, onoff):
        #turn the LED n on or off
        self.dev.query(f':LED {n:d} {onoff:d}')
    
    def readACC(self):
        #read the accelerometer, which returns data as a string
        # ax ay az (space-separated floating point numbers)
        acc_str = self.dev.query(':READ:ACC?')
        acc = np.array([float(c) for c in acc_str.split()])
        return acc
    
    def readGYR(self):
        # read the gyroscope, returns similar data as accelerometer
        gyr_str = self.dev.query(':READ:GYR?')
        gyr = np.array([float(c) for c in gyr_str.split()])
        return gyr
    
    def readT(self):
        # read the temperature, the response string
        # is 100*T, where T is the temperature in celsius
        resp = self.dev.query(':READ:T?')
        return float(resp)/100

    def readP(self):
        #read pressure, in Pa
        resp = self.dev.query(':READ:P?')
        return float(resp)
    
    def shut_down(self):
        for k in range(5):
            self.led(k, 0)

    # context management special functions
    # so that the Pico class can be used in with

    #called at the entry to with block
    def __enter__(self):
        return self

    #called on exit from with block
    def __exit__(self, *args):
        # to force flush the I/O buffer, which seems to be buggy on pyvisa-py
        # probably not necessary on NI-VISA
        self.idn()
        self.shut_down()
        self.dev.close()


if __name__ == '__main__':
    import time
    rm = vi.ResourceManager()
    with Pico(rm) as device:
        device.led(2, 1)
        print("Press Ctrl-C to quit")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("Quitting")
    # at this point, device.__exit__() has run