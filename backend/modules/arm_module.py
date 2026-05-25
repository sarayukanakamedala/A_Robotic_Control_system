import serial

class RoboticArm:

    def __init__(self):

        self.ser = serial.Serial("COM3",9600)

    def move(self, gesture):

        commands = {

            "OPEN":1,
            "CLOSE":2,
            "LEFT":3,
            "RIGHT":4

        }

        if gesture in commands:

            self.ser.write(str(commands[gesture]).encode())