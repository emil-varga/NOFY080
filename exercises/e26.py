import pyvisa as vi

def find_pico(rm):
    addresses = rm.list_resources()
    for addr in addresses:
        opened = False
        try:
            # print(addr)
            dev = rm.open_resource(addr, read_termination='\n', write_termination='\n')
            opened = True
            # print('Opened:', opened)
            resp = dev.query('*IDN?')
            # print(resp)
            if resp.strip() == 'PICO':
                return dev
        except:
            if opened:
                dev.close()
    return None

if __name__ == '__main__':
    rm = vi.ResourceManager()
    dev = find_pico(rm)
    print(dev)
    dev.close()
    rm.close()