#!/usr/bin/env python3

import asyncio, subprocess

import message_pb2
import wiringpi
from motor import Motor

class MotorServerProtocol:
    def __init__(self, motors):
        self.motors = motors
    def connection_made(self, transport):
        self.transport = transport

    def datagram_received(self, data, addr):
        #VerticalJoystickPosition = message_pb2.VerticalJoystickPosition()
        v = data.decode("utf-8").split(",")
        if len(v) != 2:
            return

        index = int(v[0])
        value = float(v[1])

        if index >= 0 and index < len(self.motors):
            self.motors[index].move(value)



if __name__ == "__main__":
    wiringpi.wiringPiSetupGpio() 
    wiringpi.pwmSetMode( wiringpi.GPIO.PWM_MODE_MS )
    motor1 = Motor(22, 23)
    motor2 = Motor(24, 25)

    process = subprocess.Popen("raspivid -n -ih -t 0 -rot 0 -w 1280 -h 720 -fps 15 -b 1000000 -o - | nc -lkv4 5001",
        shell=True)

    loop = asyncio.get_event_loop()
    print("Starting UDP server")
    # One protocol instance will be created to serve all client requests
    listen = loop.create_datagram_endpoint(
		lambda: MotorServerProtocol([motor1, motor2]), local_addr=('0.0.0.0', 9999))
    transport, protocol = loop.run_until_complete(listen)

    try:
    	loop.run_forever()
    except KeyboardInterrupt:
        pass
    transport.close()
    loop.close()

    motor1.cleanup()
    motor2.cleanup()

    process.kill()
    process.wait()
		
