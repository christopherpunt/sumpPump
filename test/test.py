import RPi.GPIO as GPIO


class SumpPump:
    WATER_LOW = 0
    WATER_MID = 1
    WATER_HIGH = 2
    WATER_OVER = 3
    
    def __init__(self):
        self.state = SumpPump.WATER_LOW
    def setLow(self):
        self.state = SumpPump.WATER_LOW
    def setMid(self):
        self.state = SumpPump.WATER_MID
    def setHigh(self):
        self.state = SumpPump.WATER_HIGH
    def setOver(self):
        self.state = SumpPump.WATER_OVER
    
    def checkState(self):
        pass
    
    
        
def setGPIO(lights, inputskk):
    GPIO.setmode(GPIO.BCM)
    for light in lights:
        GPIO.setup(light, GPIO.OUT)
        GPIO.setup(light, FALSE)
    for input in inputs:
        GPIO.setup(input, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        

light1 = 14
light2 = 15
light3 = 18
light4 = 23
lights = [light1, light2, light3, light4]

input1 = 6
input2 = 13
input3 = 19
input4 = 26
inputs = [input1, input2, input3, input4]

setGPIO(lights, inputs)



#wait until an interrupt occurs
while(True):
    pass

GPIO.cleanup()
