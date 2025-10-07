import pyvisa as vi

rm = vi.ResourceManager()

print("Available resources:")
resources = rm.list_resources()
for k, res in enumerate(resources):
    print(f'VISA address {k}: {res}')

#assuming that our pico is on the last address (usually the case)
pico = rm.open_resource(resources[-1],
                        read_termination='\n',
                        write_termination='\n')
print("Identification of the last device:")
pico.write('*IDN?')
resp = pico.read()
print(resp)

# performs the same in one step
# query = write + read
print("IDN via query:")
print(pico.query("*IDN?"))

pico.close()
rm.close()

