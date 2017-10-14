#!/usr/bin/env python3
from time import sleep
import wiringpi

PWM_RANGE = 100
LOW_LIMIT = 0.2

class Motor:
    def __init__(self, gpio1, gpio2):
        self.gpio1 = gpio1
        self.gpio2 = gpio2
        wiringpi.pinMode(self.gpio1, 1)
        wiringpi.pinMode(self.gpio2, 1)
        wiringpi.softPwmCreate(self.gpio1, 0, PWM_RANGE)
        wiringpi.softPwmCreate(self.gpio2, 0, PWM_RANGE)

    def move(self, direction):
        if abs(direction) < LOW_LIMIT:
            v1 = 0
            v2 = 0
        elif direction > 0:
            v1 = 0
            v2 = min(int(PWM_RANGE*abs(direction)), PWM_RANGE)
        elif direction < 0 :
            v1 = min(int(PWM_RANGE*abs(direction)), PWM_RANGE)
            v2 = 0
        else:
            v1 = 0
            v2 = 0

        wiringpi.softPwmWrite(self.gpio1, v1)
        wiringpi.softPwmWrite(self.gpio2, v2)

    def cleanup(self):
        wiringpi.pinMode(self.gpio1,0)
        wiringpi.pinMode(self.gpio2,0)


if __name__ == "__main__":
    wiringpi.wiringPiSetupGpio() 
    wiringpi.pwmSetMode( wiringpi.GPIO.PWM_MODE_MS )
    motor = Motor(22, 23)

    try:
        while True:
            motor.move(1)
            sleep(1)
            motor.move(0)
            sleep(1)
            motor.move(-1)
            sleep(1)
            motor.move(0)
            sleep(1)

    except KeyboardInterrupt:
        pass

    motor.cleanup()
