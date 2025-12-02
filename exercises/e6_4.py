import pyvisa as vi
from Pico import Pico
import time
import numpy as np

# turn on the LEDs from 0 to n
# and turn off the LEDs from n to 5
def led_indicate(pico, angle):
    n = int(2*angle/90)
    if n > 2:
        n = 2
    elif n < -2:
        n = -1

    if n >= 0:
        for k in range(2, 3+n):
            pico.led(k, 1)
        for k in range(3+n, 5):
            pico.led(k, 0)
        for k in range(0, 2):
            pico.led(k, 0)
    if n < 0:
        for k in range(2, 1+n, -1):
            pico.led(k, 1)
        for k in range(1+n, -1, -1):
            pico.led(k, 0)
        for k in range(3, 5):
            pico.led(k, 0)


if __name__ == '__main__':
    rm = vi.ResourceManager()
    print("Measuring tilt, Ctrl-C to quit")
    try:
        with Pico(rm) as pico:
            try:
                #first get the reference accelration vector
                #by calibrating for 1 second
                print("Calibrating orientation, do not move")
                t0 = time.time()
                acc_ref = 0
                n = 0
                while time.time() - t0 < 1:
                    acc_ref += pico.readACC()
                    n += 1
                acc_ref /= n
                #we only want tilt in along the y-axs (i.e., rotation around x-axis)
                #zero out the x-component for the dot product
                acc_ref[0] = 0
                while True:
                    acc = pico.readACC()
                    acc[0] = 0
                    # calculate the angle between the reference acceleration vector and the one measured
                    angle = np.arccos(np.dot(acc, acc_ref)/np.linalg.norm(acc)/np.linalg.norm(acc_ref))
                    angle *= np.sign(acc[1] - acc_ref[1])
                    angle = angle/np.pi*180
                    print(f"{angle:.2f}")
                    led_indicate(pico, angle)
                    time.sleep(0.1)
            except KeyboardInterrupt:
                print("quitting")
    finally:
        rm.close()