import numpy as np
import pyvisa
import time

rm = pyvisa.ResourceManager()
resources = rm.list_resources()

pico = rm.open_resource(resources[-1], read_termination='\n',
                        write_termination='\n')

try:
    temperature = float(pico.query(':READ:T?'))/100
    pressure = float(pico.query(':READ:P?'))
    acc_resp = pico.query(':READ:ACC?')
    rot_resp = pico.query(':READ:GYR?')
    acc = np.array([float(x) for x in acc_resp.split(' ')])/2**14
    rot = np.array([float(x) for x in rot_resp.split(' ')])/2**14
    
    
    print(f"The temperature is {temperature} deg C.")
    print(f"The pressure is {pressure} Pa.")
    print(f"The acceleration vector is {acc}g.")
    print(f"The rotation vector is {rot}.")
    
    led_id = 0
    while True:
        pico.query(f":LED {led_id} 1")
        time.sleep(0.25)
        pico.query(f":LED {led_id} 0")
        led_id = (led_id + 1) % 5
finally:
    for led_id in range(5):
        pico.query(f':LED {led_id} 0')