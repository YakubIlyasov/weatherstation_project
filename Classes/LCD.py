import RPi.GPIO as GPIO
import time


class LCD():
    def __init__(self, rs, rw, e, d7, d6, d5, d4, d3=0, d2=0, d1=0, d0=0):
        self.__lst_filter = [0x80, 0x08]
        self.__lst_pinout = [rs, rw, e, d7, d6, d5, d4, d3, d2, d1, d0]

        for index in range(0, len(self.__lst_pinout)):
            GPIO.setup(self.__lst_pinout[index], GPIO.OUT)

        self.__reset()
        self.__function_set()
        self.__display_on()
        self.clear_display_and_cursor_home()
        self.__send_data_to_lcd(0b00001100)  # turns of cursor

    def __enable_transfer(self, mode):  # transfer data to lcd
        GPIO.output(self.__lst_pinout[0], mode)  # rs depends on data being instruction or not
        GPIO.output(self.__lst_pinout[1], False)  # rw low
        GPIO.output(self.__lst_pinout[2], True)  # e high
        time.sleep(0.0005)  # delay to make sure data was transfered well
        GPIO.output(self.__lst_pinout[2], False)  # e low

    def __send_data_to_lcd(self, data, mode=False):  # send data or instruction to lcd
        index = 0  # index for filter in lst_filter
        while index < 2:  # go trough both filters
            filter = self.__lst_filter[index]
            for bit in range(3, len(self.__lst_pinout)):
                GPIO.output(self.__lst_pinout[bit], data & filter)
                filter >>= 1  # move filter bit one place to the right

            self.__enable_transfer(mode)  # transfer data to lcd

            index += 1
            time.sleep(0.005)

    def __reset(self):
        time.sleep(0.005)
        self.__send_data_to_lcd(0x33)
        time.sleep(0.0015)
        self.__send_data_to_lcd(0x32)
        time.sleep(0.005)
        self.__send_data_to_lcd(0x28)
        time.sleep(0.00015)
        self.__send_data_to_lcd(0x08)
        time.sleep(0.00015)
        self.__send_data_to_lcd(0x01)
        time.sleep(0.00015)
        self.__send_data_to_lcd(0x06)
        time.sleep(0.00015)

    def __function_set(self):
        self.__send_data_to_lcd(0x28)
        time.sleep(0.005)

    def __display_on(self):
        self.__send_data_to_lcd(0x0F)
        time.sleep(0.005)

    def move_cursor_to_position(self, ddram_adres=0):  # from 0 until 15 or from 64 until 79 (0x00 until 0x0f or from 0x40 until 0x4f)
        # db7: must be high
        # db6 - db0: ddram adres
        if ddram_adres >= 0 and ddram_adres <= 15 or ddram_adres >= 64 and ddram_adres <= 79:
            self.__send_data_to_lcd(ddram_adres | 0x80)  # db7, db6, db5, db4, db3, db2, db1, db0

    def send_text_to_lcd(self, text):
        for character in str(text):
            self.__send_data_to_lcd(ord(character), True)

    def clear_display_and_cursor_home(self):
        self.__send_data_to_lcd(0x01)
        time.sleep(0.005)
