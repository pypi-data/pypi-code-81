import os 
import RPi.GPIO as GPIO
import time

'''
Pinled เป็น (Green, Yello, Red) [Drive , Initial or Emer, Stop]
Pinmotor เป็น (PWM0, GPIO0, PWM1, GPIO19)

'''
class Car:
    def __init__(self, led=[17, 27, 22], motor=[12, 6, 13, 19], irsensor= [2, 3], buzzer= 4):
        self.led = led
        self.motor = motor
        self.irsensor = irsensor
        self.buzzer = buzzer
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(irsensor[0], GPIO.IN)
        GPIO.setup(irsensor[1], GPIO.IN)
        GPIO.setup(motor[0], GPIO.OUT)
        GPIO.setup(motor[1], GPIO.OUT)
        GPIO.setup(motor[2], GPIO.OUT)
        GPIO.setup(motor[3], GPIO.OUT)
        GPIO.setup(led[0], GPIO.OUT)
        GPIO.setup(led[1], GPIO.OUT)
        GPIO.setup(led[2], GPIO.OUT)
        GPIO.setup(buzzer, GPIO.OUT)
    
    def WaitObjects(self, label):
        self.status = 0
        while self.status == 0:
            GPIO.output(self.motor[0], 0)
            GPIO.output(self.motor[1], 1)
            GPIO.output(self.motor[2], 1)
            GPIO.output(self.motor[3], 0)
            if self.label == "person":
                self.status = 1
                break
            else : 
                continue

        return self.status
        
    def FindObjects(self, label):
        self.status = 0
        while self.status == 0:
            GPIO.output(self.motor[0], 0)
            GPIO.output(self.motor[1], 1)
            GPIO.output(self.motor[2], 1)
            GPIO.output(self.motor[3], 0)
            if self.label == "person":
                self.status = 1
                break
            else : 
                continue

        return self.status
    
    def Stop(self):   
        GPIO.output(self.motor[0], 0)
        GPIO.output(self.motor[1], 0)
        GPIO.output(self.motor[2], 0)
        GPIO.output(self.motor[3], 0)
        GPIO.output(self.led[2], 1)
        GPIO.output(self.led[0], 0)
        GPIO.output(self.led[1], 0)
        print("Stop")
            
    def Forward(self):
        GPIO.output(self.motor[0], 0)
        GPIO.output(self.motor[1], 1)
        GPIO.output(self.motor[2], 0)
        GPIO.output(self.motor[3], 1)
        GPIO.output(self.led[0], 1)
        GPIO.output(self.led[0], 0)
        GPIO.output(self.led[2], 0)
        print("Forward")

    def Reverse(self):
        GPIO.output(self.motor[0], 1)
        GPIO.output(self.motor[1], 0)
        GPIO.output(self.motor[2], 1)
        GPIO.output(self.motor[3], 0)
        GPIO.output(self.led[1], 1)
        GPIO.output(self.led[0], 0)
        GPIO.output(self.led[2], 0)
        print("Reverse")

    def TurnLeft(self):
        GPIO.output(self.motor[0], 0)
        GPIO.output(self.motor[1], 0)
        GPIO.output(self.motor[2], 0)
        GPIO.output(self.motor[3], 1)
        GPIO.output(self.led[0], 1)
        GPIO.output(self.led[1], 0)
        GPIO.output(self.led[2], 0)
        print("Turn Left")               	

    def TurnRight(self):
        GPIO.output(self.motor[0], 0)
        GPIO.output(self.motor[1], 0)
        GPIO.output(self.motor[2], 1)
        GPIO.output(self.motor[3], 0)
        GPIO.output(self.led[0], 1)
        GPIO.output(self.led[1], 0)
        GPIO.output(self.led[2], 0)
        print("Turn Right")

        	
    def End(self):
        GPIO.cleanup()

    def PlaySound(self, sound):
        os.system(self.sound)

if __name__ == '__main__':

    car = Car()
    car.Forward()
    car.Reverse()