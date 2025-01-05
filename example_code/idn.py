import pyvisa as visa
rm = visa.ResourceManager()
pico = rm.open_resource('ASRL/dev/ttyACM0::INSTR',
                        read_termination='\n',
                        write_termination='\n')
print(pico.query('*IDN?'))
pico.close()
rm.close()