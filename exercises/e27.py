import time
import pyvisa as vi

import e26

rm = vi.ResourceManager("@py")

# pico = rm.open_resource('ASRL5::INSTR', timeout=1000,
#                         read_termination='\n',
#                         write_termination='\n')

pico = e26.find_pico(rm)

try:
    t0 = time.time()
    while True:
        pico.query(':LED 3 1')
        time.sleep(0.1)
        pico.query(':LED 3 0')
        time.sleep(0.1)
        pico.query(':LED 4 1')
        time.sleep(0.1)
        pico.query(':LED 4 0')
        time.sleep(0.1)
        if time.time() - t0 > 10:
            break
finally:
    for led in range(5):
        pico.query(f':LED {led} 0')
    pico.close()
    rm.close()