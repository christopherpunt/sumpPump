import time
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import threading

BROKER = 'iot.cs.calvin.edu'
USERNAME = "cs300" # Put broker username here
PASSWORD = "safeIoT"
TOPIC = 'chris/pump'
CERTS = '/etc/ssl/certs/ca-certificates.crt'
PORT = 8883
QOS = 0

MAIN_THREAD_DELAY = 5
TIMERLEN = 6

NORMAL = 1
OVERFLOWING = 2
POWEROUTAGE = 3
INTERNETOUTAGE = 4


state = NORMAL
stateList = [NORMAL, OVERFLOWING, INTERNETOUTAGE]

LEDLOW = 17
LEDMID = 27
LEDHIGH = 22
LEDOVER = 23
LEDs = [LEDLOW,LEDMID,LEDHIGH,LEDOVER]

GPIO.setmode(GPIO.BCM) # Use BCM numbers
GPIO.setup(LEDLOW, GPIO.OUT)
GPIO.setup(LEDMID, GPIO.OUT)
GPIO.setup(LEDHIGH, GPIO.OUT)
GPIO.setup(LEDOVER, GPIO.OUT)

global t

def timeout():
    state = INTERNETOUTAGE
    print("time expired")
    #sendEmail
    global t
    t.cancel()

t = threading.Timer(TIMERLEN, timeout)
t.start()

def turnOneLEDOn(myled):
    global LEDs
    for led in LEDs:
        GPIO.output(led, False)
    GPIO.output(myled, True)

turnOneLEDOn(LEDLOW)

# Callback when connecting to the MQTT broker
def on_connect(client, userdata, flags, rc):
    if rc==0:
        print('Connected to',BROKER)
    else:
        print('Connection to',BROKER,'failed. Return code=',rc)
        exit(1)


# Callback when client receives a PUBLISH message from the broker
def on_message(client, data, msg):
    global t
    global state
    normalList = ["low", "mid", "high"]
    if msg.topic == TOPIC:
        message = msg.payload.decode("utf-8")
        #if there was an internet outage
        if state == INTERNETOUTAGE:
            if message in normalList:
                state = NORMAL
            elif message == "over":
                state = OVERFLOWING
            #send email saying reconnected

        else: #state != INTERNETOUTAGE
            if message in normalList:
                state = NORMAL
                #reset timer            
                t.cancel()
                t = threading.Timer(TIMERLEN, timeout)
                t.start()
                print()
                
                if message == "low":
                    turnOneLEDOn(LEDLOW)
                    print("NORMAL: low")
                elif message == "mid":
                    turnOneLEDOn(LEDMID)
                    print("NORMAL: mid")
                elif message == "high":
                    turnOneLEDOn(LEDHIGH)
                    print("NORMAL: high")
                else:
                    turnOneLEDOn(LEDOVER)
                    print("ERROR! I don't know what happened")

            elif message == "over":
                state = OVERFLOWING
                #reset timer
                t.cancel()
                t = threading.Timer(TIMERLEN, timeout)
                t.start()
                turnOneLEDOn(LEDOVER)
                #sendEmail()
                print("the pump is overflowing LEAVE NOW, sending email")
            elif message == "connected":
                t.cancel()
                t = threading.Timer(TIMERLEN, timeout)
                t.start()
                print("still connected")
            else:
                print("Error: unrecognized message = " + message)

        
# Setup MQTT client and callbacks
client = mqtt.Client()
client.username_pw_set(USERNAME, password=PASSWORD)
client.tls_set(CERTS)
client.on_connect = on_connect
client.on_message = on_message

# Connect to MQTT broker and subscribe to the button topic
client.connect(BROKER, PORT, 60)
client.subscribe(TOPIC, qos=QOS)
client.loop_start()


try:
    while True:
        time.sleep(MAIN_THREAD_DELAY)
        

except KeyboardInterrupt:
    print("\nDone")
    GPIO.cleanup()
    client.disconnect()