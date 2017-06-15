# libraries
import RPi.GPIO as GPIO
import time
from datetime import datetime
from threading import Timer
from Classes import MCP
from Classes import LCD
from Classes import Database_class
from Classes import HDC1080
from Classes import time_local_time
from Classes import math_operations

GPIO.setmode(GPIO.BCM)  # use BCM pinout

# declare variabeles
lst_air_quality = []  # list for air quality measurements
lst_humidity = []  # list for humidity measurements
lst_light = []  # list for light measurements
lst_temperature = []  # list for temperature measurements

time_now = ""  # time for logging
counter = 0  # counter for lcd routine

# declare lcd pins
pin_rs = 16
pin_rw = 20
pin_e = 21
pin_d4 = 6
pin_d5 = 13
pin_d6 = 19
pin_d7 = 26


def send_data_to_database():  # send measurements to database
    global lst_air_quality, lst_humidity, lst_light, lst_temperature, time_now  # use global variables

    # calculate mean of first 60 values in list (60 for every minute in an hour)
    air_quality = math_operations.math_operations.mean(lst_air_quality[0:60])
    humidity = math_operations.math_operations.mean(lst_humidity[0:60])
    light = math_operations.math_operations.mean(lst_light[0:60])
    temperature = math_operations.math_operations.mean(lst_temperature[0:60])

    # send data to database table measurement
    database_weatherstation.set_data_to_table_measurement(air_quality, 1)
    database_weatherstation.set_data_to_table_measurement(humidity, 2)
    database_weatherstation.set_data_to_table_measurement(light, 3)
    database_weatherstation.set_data_to_table_measurement(temperature, 4)

    # get data from table measurement, take the last tuple in that list, then take the first number from it
    index_value = database_weatherstation.get_data_from_database("measurement")[-1][0]

    # send data to database table weatherstation
    database_weatherstation.set_data_to_table_weatherstation(time_now, index_value - 3)
    database_weatherstation.set_data_to_table_weatherstation(time_now, index_value - 2)
    database_weatherstation.set_data_to_table_weatherstation(time_now, index_value - 1)
    database_weatherstation.set_data_to_table_weatherstation(time_now, index_value)

    # reset lists
    lst_air_quality = []
    lst_humidity = []
    lst_light = []
    lst_temperature = []


try:  # main programme
    # create objects
    local_time = time_local_time.time_local_time()  # create time object
    analog_sensor = MCP.SPI()  # create analog sensor object
    digital_sensor = HDC1080.HDC1080()  # create digital sensor object
    database_weatherstation = Database_class.Database_class()  # create database object
    lcd = LCD.LCD(pin_rs, pin_rw, pin_e, pin_d7, pin_d6, pin_d5, pin_d4, 0, 0, 0, 0)  # create lcd object

    time_now = time_local_time.time_local_time().get_local_time()  # get time

    while True:  # main loop
        # get sensor values
        air_quality = MCP.Analog.value_to_percentage(MCP.Analog.value_to_voltage(analog_sensor.readChannel(0), 1023, 5.0), 5.0)
        humidity = digital_sensor.read_humidity()
        light = MCP.Analog.value_to_percentage(MCP.Analog.value_to_voltage(analog_sensor.readChannel(1), 1023, 5.0), 5.0)
        temperature = digital_sensor.read_temperature()

        # add value to list with measurements from sensor
        lst_air_quality.append(air_quality)
        lst_humidity.append(humidity)
        lst_light.append(light)
        lst_temperature.append(temperature)

        if time_now != time_local_time.time_local_time().get_local_time():  # check if minute has passed
            time_now = time_local_time.time_local_time().get_local_time()  # save time at this moment
            send_data_to_database()  # send measurements to database

        lcd.clear_display_and_cursor_home()  # clear lcd display and set cursor to home position

        if counter == 2:  # check counter value
            counter = 0  # reset counter

        if counter == 0:  # display air quality and humidity
            lcd.send_text_to_lcd("Air: %.2f%s" % (air_quality, '%'))
            lcd.move_cursor_to_position(64)  # move cursor to second line
            lcd.send_text_to_lcd("Humidity: %.2f%s" % (humidity, '%'))

        elif counter == 1:  # display light and temperature
            lcd.send_text_to_lcd("Light: %.2f%s" % (light, '%'))
            lcd.move_cursor_to_position(64)  # move cursor to second line
            lcd.send_text_to_lcd("Temp: %.2f %s" % (temperature, 'C'))

        counter += 1  # increase counter
        time.sleep(1)  # delay for lcd and sensor measurements

except KeyboardInterrupt:  # code during exception
    lcd.clear_display_and_cursor_home()
    lcd.send_text_to_lcd("weatherstation")
    lcd.move_cursor_to_position(64)
    lcd.send_text_to_lcd(".py has stopped.")
    analog_sensor.close_spi()
    GPIO.cleanup()

finally:  # code after exception
    lcd.clear_display_and_cursor_home()
    lcd.send_text_to_lcd("weatherstation")
    lcd.move_cursor_to_position(64)
    lcd.send_text_to_lcd(".py has stopped.")
    analog_sensor.close_spi()
    GPIO.cleanup()
