from machine import Pin, I2C, ADC, PWM

import network
import socket

import json

from utime import sleep_ms


with open("conf.json") as f:
    conf = json.load(f)

# wifi (only for W ver)
WIFI_SSID = conf["global"]["wi_fi"]["ssid"]
WIFI_PASSWORD = conf["global"]["wi_fi"]["password"]

# cooler params
COOLER_PWM_PIN = conf["project"]["pwm_pin"]
COOLER_PWM_FREQ = conf["project"]["pwm_freq"]
DUTY_MAX = conf["project"]["duty_max"]
DUTY_MIN = conf["project"]["duty_min"]

# temp params
TEMP_TABLE = conf["project"]["temp_table"]
TEMP_FACTOR = conf["project"]["temp_factor"]
TEMP_FACTOR_ARG = conf["project"]["temp_factor_arg"]


class Temperature:
        def __init__(self):
                self.sensor = ADC(4)
                self.factor = 3.3 / (65535)

        def data(self) -> float:
                reading = self.sensor.read_u16() * self.factor    
                return round(27 - (reading - 0.706)/0.001721,2)  


class Cooler:
        def __init__(self, pin: int = 4, freq: int = 1000, duty: int = 20000):
                self.pwm = PWM(Pin(pin), freq=freq, duty_u16=duty)

        def set_speed(self, duty: int):
                self.pwm.duty_u16(duty)


class WiFi:
        def __init__(self, ssid: str, password: str):
                self.ssid = ssid
                self.password = password


tsensor = Temperature()
cooler = Cooler(pin=COOLER_PWM_PIN, freq=COOLER_PWM_FREQ, duty=DUTY_MIN)
wifi = WiFi(WIFI_SSID, WIFI_PASSWORD)



print("Starting Now")
      
while True:
        tmprtr = tsensor.data()
        # print(tmprtr)
        sleep_ms(500)

        if TEMP_FACTOR and TEMP_FACTOR_ARG > 0:
                duty = round(DUTY_MIN + tmprtr * TEMP_FACTOR_ARG)
                print(tmprtr, " - ", duty)
                cooler.set_speed(duty)
        else:
                for tparam in TEMP_TABLE:
                        if tmprtr > tparam["temp_min"] and tmprtr <= tparam["temp_max"]:
                                cooler.set_speed(tparam["duty"])
                                print(tmprtr, " - ", tparam["duty"])
                                break
                        else:
                                continue