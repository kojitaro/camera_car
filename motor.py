#!/usr/bin/env python3
from time import sleep
import wiringpi



class Motor:
    def __init__(self, gpio1, gpio2):
        self.gpio1 = gpio1
        self.gpio2 = gpio2
        wiringpi.pinMode(self.gpio1, 1)
        wiringpi.pinMode(self.gpio2, 1)
        wiringpi.softPwmCreate(self.gpio1, 0, 100)
        wiringpi.softPwmCreate(self.gpio2, 0, 100)

    def move(self, direction):
        if direction > 0:
            wiringpi.softPwmWrite(self.gpio1, 0)
            wiringpi.softPwmWrite(self.gpio2, 70)
        elif direction < 0 :
            wiringpi.softPwmWrite(self.gpio1, 70)
            wiringpi.softPwmWrite(self.gpio2, 0)
        else:
            wiringpi.softPwmWrite(self.gpio1, 0)
            wiringpi.softPwmWrite(self.gpio2, 0)
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
