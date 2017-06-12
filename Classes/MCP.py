# libraries
import spidev


class SPI:  # use spi bus
    def __init__(self, port=0, cs=0):  # init spi
        # open SPI bus
        self.__spi = spidev.SpiDev()  # create spi object
        self.__spi.open(port, cs)  # open spi port, device (CS)
        return

    def close_spi(self):  # close spi bus
        return self.__spi.close()  # close spi bus

    def readChannel(self, channel):  # function to read SPI data from MCP3008 chip (channel 0 to 7)
        # 3 bytes versturen
        # 1, S D2 D1 D0 xxxx, 0
        adc = self.__spi.xfer2([1, (8 + channel) << 4, 0])
        data = ((adc[1] & 3 << 8) | adc[2])  # in byte 1 en 2 zit resultaat
        return data


class Analog:  # klasse met enkele analoge conversie functies
    @staticmethod
    def value_to_percentage(value, max_value):  # verander waarde naar waarde in procent
        return 100 - value / float(max_value) * 100.0

    @staticmethod
    def value_to_voltage(value, max_value, max_voltage):  # verander waarde naar waarde in spanning
        return value / float(max_value) * max_voltage

    @staticmethod
    def value_to_temperature_lm35(value_voltage):  # verander waarde naar waarde in graden celsius voor de LM35
        # 10 mv = 1°C
        return value_voltage / 0.01  # spanning / 10 / 1000 (=0.01)
