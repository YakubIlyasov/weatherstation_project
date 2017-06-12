# constants
HDC1080_address = 0x40  # I2C address (0100 0000)

# registers
HDC1080_temperature_register = 0x00
HDC1080_humidity_register = 0x01
HDC1080_configuration_register = 0x02
HDC1080_manufacturer_id_register = 0xFE
HDC1080_device_id_register = 0xFF
HDC1080_serial_id_high_register = 0xFB
HDC1080_serial_id_mid_register = 0xFC
HDC1080_serial_id_bottom_register = 0xFD

# Configuration Register Bits
HDC1080_config_reset_bit = 0x8000
HDC1080_config_heater_enable = 0x2000
HDC1080_config_aquisition_mode = 0x1000
HDC1080_config_battery_status = 0x0800
HDC1080_config_temperature_resolution = 0x0400
HDC1080_config_humidity_resolution_high_bit = 0x0200
HDC1080_config_humidity_resolution_low_bit = 0x0100

HDC1080_config_temperature_resolution_14_bit = 0x0000
HDC1080_config_temperature_resolution_11_bit = 0x0400

HDC1080_config_humidity_resolution_14_bit = 0x0000
HDC1080_config_humidity_resolution_11_bit = 0x0100
HDC1080_config_humidity_resolution_8_bit = 0x0200

# libraries
import smbus
import time


class HDC1080:
    def __init__(self, twi=1, address=HDC1080_address):  # init sensor
        self.__bus = smbus.SMBus(twi)
        self.__address = address
        self.__bus.write_byte_data(HDC1080_address, HDC1080_configuration_register, HDC1080_config_aquisition_mode >> 8)

    def read_temperature(self):  # read temperature from sensor
        self.__bus.write_byte(HDC1080_address, HDC1080_temperature_register)  # send temperature measurement command
        time.sleep(0.020)  # delay

        # read data
        nible_left = self.__bus.read_byte(HDC1080_address)
        nible_right = self.__bus.read_byte(HDC1080_address)

        # calculate temperature
        temperature = nible_left << 8 | nible_right
        c_temperature = temperature / 65536.0 * 165.0 - 40
        return c_temperature  # return temperature

    def read_humidity(self):  # read humidity from sensor
        self.__bus.write_byte(HDC1080_address, HDC1080_humidity_register)  # send humidity measurement command
        time.sleep(0.020)  # delay

        # read data
        nible_left = self.__bus.read_byte(HDC1080_address)
        nible_right = self.__bus.read_byte(HDC1080_address)

        # calculate humidity
        humidity = nible_left << 8 | nible_right
        humidity = humidity / 65536.0 * 100.0
        return humidity  # return humidity

    def read_config_register(self):  # read configuration from sensor
        self.__bus.write_byte(HDC1080_address, HDC1080_configuration_register)  # send command
        data = self.__bus.read_byte(HDC1080_address)  # read data
        return data  # return data

    def heater_On(self):  # turn heater on
        config = self.read_config_register()  # read config register
        config = config << 8 | HDC1080_config_heater_enable  # enable heater bit
        self.__bus.write_byte_data(HDC1080_address, HDC1080_configuration_register, config >> 8)  # send command

    def heater_off(self):  # turn heater off
        config = self.read_config_register()  # read config register
        config = config << 8 & ~HDC1080_config_heater_enable  # disable heater bit
        self.__bus.write_byte_data(HDC1080_address, HDC1080_configuration_register, config >> 8)  # send command

    def set_humidity_resolution(self, resolution):  # set the resolution for humidity readings
        config = self.read_config_register()  # read config register
        config = (config << 8 & ~0x0300) | resolution  # set resolution
        self.__bus.write_byte_data(HDC1080_address, HDC1080_configuration_register, config >> 8)  # send command

    def set_temperature_resolution(self, resolution):  # set the resolution for temperature readings
        config = self.read_config_register()  # read config register
        config = (config << 8 & ~0x0400) | resolution  # set resolution
        self.__bus.write_byte_data(HDC1080_address, HDC1080_configuration_register, config >> 8)  # send command

    def read_battery_status(self):  # read battery status
        config = self.read_config_register()  # read config register
        config = config << 8 & ~ HDC1080_config_heater_enable  # determine config

        if config == 0:  # check config status
            return True
        else:
            return False

    def read_manufacturer_id(self):  # read manufacturer id
        data = self.__bus.read_i2c_block_data(HDC1080_address, HDC1080_manufacturer_id_register, 2)  # read data
        return data[0] << 8 | data[1]  # return data

    def read_device_id(self):  # read device id
        data = self.__bus.read_i2c_block_data(HDC1080_address, HDC1080_device_id_register, 2)  # read data
        return data[0] << 8 | data[1]  # return data

    def read_serial_number(self):  # read serial number
        data = self.__bus.read_i2c_block_data(HDC1080_address, HDC1080_serial_id_high_register, 2)  # read high part
        serial_number = data[0] << 8 | data[1]  # calculate serial number

        data = self.__bus.read_i2c_block_data(HDC1080_address, HDC1080_serial_id_mid_register, 2)  # read mid part
        serial_number = serial_number << 8 | data[0] << 8 | data[1]  # calculate serial number

        data = self.__bus.read_i2c_block_data(HDC1080_address, HDC1080_serial_id_bottom_register, 2)  # read bottom part
        serial_number = serial_number << 8 | data[0] << 8 | data[1]  # calculate serial number

        return serial_number  # return serial number
