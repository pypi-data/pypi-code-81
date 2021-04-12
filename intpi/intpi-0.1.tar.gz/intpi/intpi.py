import RPi.GPIO as GPIO

class Pin(object):
    def __init__(self, pin, setup=True):
        self.pin = pin

        if setup:
            GPIO.setup(pin, GPIO.output)
            GPIO.output(pin, GPIO.LOW)

    def on(self):
        GPIO.output(pin, GPIO.HIGH)
    
    def off(self):
        GPIO.output(pin, GPIO.HIGH)

class PWM_Pin(Pin):
    def __init__(self, pin, setup=True):
        super(PWM_Pin, self).__init__(pin, setup)
        self.pin = pin
        self.pwm = GPIO.PWM(self.pin, 1000)
        self.pwm.start(0)

    def off(self):
        self.pwm.ChangeDutyCycle(0)

    def low(self):
        self.pwm.ChangeDutyCycle(25)
    
    def med(self):
        self.pwm.ChangeDutyCycle(50)
    
    def high(self):
        self.pwm.ChangeDutyCycle(75)
    
    def high_pre_max(self):
        self.pwm.ChangeDutyCycle(95)
    
    def max(self):
        self.pwm.ChangeDutyCycle(100)

    def ChangeDutyCycle(self, **args)
        self.pwm.ChangeDutyCycle(**args)

class BaseMotorObject(object):
    def __init__(self, pin1, pin2):
        self.pin1 = Pin(pin1)
        self.pin2 = Pin(pin2)

    def forward(self):
        self.pin1.on()
        self.pin2.off()
    
    def backward(self):
        self.pin1.off()
        self.pin2.on()


class Motor_ENB_PWM(BaseMotorObject):
    def __init__(self, pin1, pin2, enb):
        super(Motor_ENB_PWM, self).__init__(pin1, pin2)

        self.pwm = PWM_Pin(enb)

    def low(self):
        self.pwm.ChangeDutyCycle(25)
    
    def med(self):
        self.pwm.ChangeDutyCycle(50)
    
    def high(self):
        self.pwm.ChangeDutyCycle(75)
    
    def high_pre_max(self):
        self.pwm.ChangeDutyCycle(95)
    
    def max(self):
        self.pwm.ChangeDutyCycle(100)


class Motor_PWM_pin():
    def __init__(self, pin1, pin2):
        self.pin1 = Pin(pin1)
        self.pin2 = Pin(pin2)

    def forward(self):
        self.pin1.high()
        self.pin2.off()
    
    def backward(self):
        self.pin1.off()
        self.pin2.high()
