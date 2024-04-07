from machine import Pin, I2C, ADC, PWM
from utime import sleep_ms


MAX_DUTY = 65535
MIN_DUTY = 20000


class Temperature():
        def __init__(self):
                self.sensor = ADC(4)
                self.factor = 3.3 / (65535)

        def data(self) -> float:
                reading = self.sensor.read_u16() * self.factor    
                return round(27 - (reading - 0.706)/0.001721,2)  


class Cooler:
        def __init__(self, pin: int = 4, freq: int = 1000, duty: int = MIN_DUTY):
                self.pwm = PWM(Pin(pin), freq=freq, duty_u16=duty)

        def set_speed(self, duty: int):
                self.pwm.duty_u16(duty)


tsensor = Temperature()
cooler = Cooler()

speed = PWM(Pin(4), freq=1000, duty_u16=0)

print("Starting Now")
      
while True:
        tmprtr = tsensor.data()
        sleep_ms(500)

        if tmprtr < 30:
                cooler.set_speed(MIN_DUTY)
        elif tmprtr > 30 and tmprtr < 40:
                cooler.set_speed(MIN_DUTY + 10000)
        elif tmprtr > 40 and tmprtr < 50:
                cooler.set_speed(MIN_DUTY + 20000)
        elif tmprtr > 50 and tmprtr < 60:
                cooler.set_speed(MIN_DUTY + 30000)
        elif tmprtr > 60 and tmprtr < 70:
                cooler.set_speed(MIN_DUTY + 40000)
        else:
             cooler.set_speed(MAX_DUTY)