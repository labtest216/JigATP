#!/usr/bin/python3
import smbus
import time

# SHT31D default address.
SHT31_I2CADDR = 0x45

# SHT31D Registers

SHT31_MEAS_HIGHREP_STRETCH = [0x2C, 0x06]
SHT31_MEAS_MEDREP_STRETCH = [0x2C, 0x0D]
SHT31_MEAS_LOWREP_STRETCH = [0x2C, 0x10]
SHT31_MEAS_HIGHREP = [0x24, 0x00]
SHT31_MEAS_MEDREP = [0x24, 0x0B]
SHT31_MEAS_LOWREP = [0x24, 0x16]
SHT31_READSTATUS = [0xF3, 0x2D]
SHT31_CLEARSTATUS = [0x30, 0x41]
SHT31_SOFTRESET = [0x30, 0xA2]
SHT31_HEATER_ON = [0x30, 0x6D]
SHT31_HEATER_OFF = [0x30, 0x66]

SHT31_STATUS_DATA_CRC_ERROR = [0x00, 0x01]
SHT31_STATUS_COMMAND_ERROR = [0x00, 0x02]
SHT31_STATUS_RESET_DETECTED = [0x00, 0x10]
SHT31_STATUS_TEMPERATURE_ALERT = [0x04, 0x00]
SHT31_STATUS_HUMIDITY_ALERT = [0x08, 0x00]
SHT31_STATUS_HEATER_ACTIVE = [0x20, 0x00]
SHT31_STATUS_ALERT_PENDING = [0x80, 0x00]


class SSHT31(object):
    def __init__(self, address, i2c_bus):
        # Get I2C bus number and address.
        self._addr = address
        self._bus = smbus.SMBus(i2c_bus)

    def write_command(self, cmd):
        self._bus.write_i2c_block_data(self._addr, cmd[0], [cmd[1]])

    def reset(self):
        self.write_command(SHT31_SOFTRESET)
        time.sleep(0.01)  # Wait the required time

    def clear_status(self):
        self.write_command(SHT31_CLEARSTATUS);

    def read_status(self):
        self.write_command(SHT31_READSTATUS);
        buffer = self._bus.read_i2c_block_data(self._addr, 0x00, 3)

        stat = buffer[0] << 8 | buffer[1]
        if buffer[2] != self._crc8(buffer[0:2]):
            return None
        return stat

    def is_data_crc_error(self):
        return bool(self.read_status() & SHT31_STATUS_DATA_CRC_ERROR)

    def is_command_error(self):
        return bool(self.read_status() & SHT31_STATUS_COMMAND_ERROR)

    def is_reset_detected(self):
        return bool(self.read_status() & SHT31_STATUS_RESET_DETECTED)

    def is_tracking_temperature_alert(self):
        return bool(self.read_status() & SHT31_STATUS_TEMPERATURE_ALERT)

    def is_tracking_humidity_alert(self):
        return bool(self.read_status() & SHT31_STATUS_HUMIDITY_ALERT)

    def is_heater_active(self):
        return bool(self.read_status() & SHT31_STATUS_HEATER_ACTIVE)

    def is_alert_pending(self):
        return bool(self.read_status() & SHT31_STATUS_ALERT_PENDING)

    def set_heater(self, do_enable=True):
        if do_enable:
            self.write_command(SHT31_HEATER_ON)
        else:
            self.write_command(SHT31_HEATER_OFF)

    def read_temperature_humidity(self):
        self.write_command(SHT31_MEAS_HIGHREP)
        time.sleep(0.1)
        data = self._bus.read_i2c_block_data(self._addr, 0x00, 6)

        if data[2] != self._crc8(data[0:2]):
            return (float("nan"), float("nan"))

        # Convert the data
        rawTemperature = data[0] * 256 + data[1]
        temperature = -45 + (175 * rawTemperature / 65535.0)
        ftemperature = -49 + (315 * rawTemperature / 65535.0)
        humidity = 100 * (data[3] * 256 + data[4]) / 65535.0

        if data[5] != self._crc8(data[3:5]):
            return float("nan"), float("nan")
        return temperature, ftemperature, humidity

    def read(self):
        temperature, ftemperature, humidity = self.read_temperature_humidity()
        print(str(temperature) + "[c] " + str(ftemperature) + "[f] " + str(humidity) + "[%]")
        return temperature, ftemperature, humidity

    def read_temperature(self):
        temperature, ftemperature, humidity = self.read_temperature_humidity()
        return temperature

    def read_ftempperature(self):
        temperature, ftemperature, humitity = self.read_temperature_humidity()
        return ftemperature

    def read_humidity(self):
        temperature, ftemperature, humidity = self.read_temperature_humidity()
        return humidity

    def crc8(self, buffer):
        """ Polynomial 0x31 (x8 + x5 +x4 +1) """

        polynomial = 0x31;
        crc = 0xFF;

        index = 0
        for index in range(0, len(buffer)):
            crc ^= buffer[index]
            for i in range(8, 0, -1):
                if crc & 0x80:
                    crc = (crc << 1) ^ polynomial
                else:
                    crc = (crc << 1)
        return crc & 0xFF

    def test_device(self):
        self.read()


#sht = SHT31(0x45, 2).test_device()
