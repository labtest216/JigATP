from Log.log import *
from serial import Serial
import serial.tools.list_ports
from config import *


class Device:
    _com = None
    _br = 0
    _i_init_com = None
    _test_com = {"cmd": "", "ack": ""}

    def __int__(self):
        self.logger = self.init_logger()
        if self._i_init_com:
            self.i_init_com()

    def test_device(self): pass

    def init_board(self): pass

    def i_init_com(self):
        self._com.name = self.get_com()

        if self._com.name == -1:
            self.logger.debug("init fail")
            return -1
        else:
            return self.init_com(self._com.name, self._br)

    def test_com(self):
        self._com.write(self._test_com["cmd"].encode("ascii"))
        read_buf = self._com.read(size=len(self._test_com["ack"])).decode("ascii")
        print(read_buf)

        if read_buf == self._test_com["ack"]:
            print(self.get_class_name()+":test com ack")
            return 0
        else:
            return -1

    def get_com(self):
        comlist = serial.tools.list_ports.comports()
        connected_com = []
        for element in comlist:
            connected_com.append(element.device)
        print("Connected COM ports: " + str(connected_com))

        for com in connected_com:
            if self.init_com(com, self._br) == 0:  # Try init com.
                if self.test_com() == 0:  # Try test com.
                    print(self.get_class_name() + " :" + str(com))
                    self._com.name = str(com)
                    self._com.close()
                    return str(com)
                else:  # Try next com.
                    self._com.close()
        return -1

    def init_com(self, com, br):
        try:
            self._com = Serial(port=com, baudrate=br, bytesize=8, parity='N', stopbits=1, timeout=2)#

            if self._com.is_open:
                self.logger.debug(self.debug_com_pass())
                return 0
            else:
                self.logger.debug(self.debug_com_fail())
                return -1
        except:
            return -2

    def send_and_get(self, data_to_send):
        self.logger.debug(self.get_class_name() + " send " + data_to_send)
        self._com.write(data_to_send.encode("ascii"))
        read_buf = self._com.read_until()
        return read_buf.decode()

    def send_and_wait(self, data_to_send, data_to_get):
        self.logger.debug(self.get_class_name() + " send " + data_to_send+" wait for " + data_to_get)
        self._com.write(data_to_send.encode("ascii"))
        read_buf = self._com.read(size=len(data_to_get)).decode("ascii")
        self.logger.debug(self.get_class_name() + " receive " + str(read_buf))
        if read_buf == data_to_get:
            return 0
        else:  # Try resend and wait for ack.
            self._com.write(data_to_send.encode("ascii"))
            read_buf = self._com.read(size=len(data_to_get)).decode("ascii")
            self.logger.debug(self.get_class_name() + " send " + data_to_send + " wait for " + data_to_get)
            self.logger.debug(self.get_class_name() + " receive " + str(read_buf))
            if read_buf == data_to_get:
                return 0
            else:
                self.logger.debug(self.get_class_name() + " not get ack")
                return -1

    def get_class_name(self):
        name = str(type(self).__name__)
        return name

    def debug_com_pass(self):
        return self.get_class_name() + " open " + self._com.name + " pass."

    def debug_com_fail(self):
        return self.get_class_name() + " open " + self._com.name + " fail."

    def init_logger(self):
        # Create logger.
        logger = logging.getLogger(self.get_class_name())
        logger.setLevel(logging.DEBUG)

        # Create console and file handlers and set level to debug.
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        fh = logging.FileHandler(log_path)

        # Create formatter.
        form = str(time.time()) + '  %(asctime)s  FileName=%(filename)s  FuncName=%(funcName)s:  %(message)s'
        formatter = logging.Formatter(form)

        # Add formatter.
        ch.setFormatter(formatter)
        fh.setFormatter(formatter)

        # add handlers to logger
        logger.addHandler(ch)
        logger.addHandler(fh)
        return logger