from serial import Serial
from config import *
from device import Device

class Sniffer(Device):
    _br = snif_br
    _i_init_com = 1
    _test_com = {"cmd": "Sniffer_Test_Com", "ack": "Sniffer_Ok"}
    
    def __init__(self):
        super().__int__()

    def read(self, lines, file_path):
        if snif_flag:
            f = open(file_path, 'w+')
            f.truncate()

            if self._com.is_open:
                i = 0
                while i < lines:
                    data = self._com.readline()
                    f.write(str(data))
                    if snif_flag:
                        print(data)
                    i += 1
                f.close()
                self._com.close()
                print("Communication with sniffer close.")
            else:
                print("Com can not open, Communication with sniffer fail.")

# Test class.
s = Sniffer()