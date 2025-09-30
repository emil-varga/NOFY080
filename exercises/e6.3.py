import pyvisa as vi
from Pico import Pico
import time

# turn on the LEDs from 0 to n
# and turn off the LEDs from n to 5
def led_indicate(pico, n):
    for k in range(0, n):
        pico.led(k, 1)
    for k in range(n, 5):
        pico.led(k, 0)

# normalize the temperature to (Tmin,Tmax)
# interval, clipping the edges
def normalize(T, Tmin=20, Tmax=27):
    if T < Tmin:
        return 0
    if T > Tmax:
        return 5
    return int(5*(T-Tmin)/(Tmax - Tmin))

Tmin = 20
Tmax = 27
Toverheat = 28

if __name__ == '__main__':
    rm = vi.ResourceManager()
    print("Measuring temperature, Ctrl-C to quit")
    try:
        with Pico(rm) as pico:
            try:
                while True:
                    T = pico.readT()
                    print(T)
                    led_indicate(pico, normalize(T, Tmin, Tmax))
                    if T > Toverheat:
                        raise RuntimeError("Overheating.")
            except KeyboardInterrupt:
                print("quitting")
    finally:
        rm.close()