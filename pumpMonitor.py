import time
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import send_emails

BROKER = 'iot.cs.calvin.edu'
USERNAME = "cs300" # Put broker username here
PASSWORD = "safeIoT"
TOPIC = 'chris/pump'
CERTS = '/etc/ssl/certs/ca-certificates.crt'
PORT = 8883
QOS = 0

MAIN_THREAD_DELAY = 5

operational = 1
powerOutage = 2
internetOutage = 3

state = operational
stateList = [operational, powerOutage, internetOutage]

#constants
FLOATLOW = 21
FLOATMID = 20
FLOATHIGH = 16
FLOATOVER = 26
glitchFilter = 100

# Setup GPIO mode
GPIO.setmode(GPIO.BCM)
# Configure GPIO input
GPIO.setup(FLOATLOW, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(FLOATMID, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(FLOATHIGH, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(FLOATOVER, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Callback when connecting to the MQTT broker
def on_connect(client, userdata, flags, rc):
    if rc==0:
        print('Connected to',BROKER)
    else:
        print('Connection to',BROKER,'failed. Return code=',rc)
        exit(1)

# Callback when a message is published
def on_publish(client, userdata, mid):
    print("MQTT data published")

# Callback when client receives a PUBLISH message from the broker
def on_message(client, data, msg):
    if msg.topic == TOPIC:
        print("Received message: LED = ", int(msg.payload))
        

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

def levelListener(channel):
    if channel == FLOATLOW:
        print("FLOATLOW")
    elif channel == FLOATMID:
        print("FLOATMID")
    elif channel == FLOATHIGH:
        print("FLOATHIGH")
    elif channel == FLOATOVER:
        print("****the sump pump is overflowing!****")

GPIO.add_event_detect(FLOATLOW, GPIO.RISING, callback=levelListener, bouncetime=100)
GPIO.add_event_detect(FLOATMID, GPIO.RISING, callback=levelListener, bouncetime=100)
GPIO.add_event_detect(FLOATHIGH, GPIO.RISING, callback=levelListener, bouncetime=100)
GPIO.add_event_detect(FLOATOVER, GPIO.RISING, callback=levelListener, bouncetime=100)

try:
    while True:
        time.sleep(MAIN_THREAD_DELAY)

except KeyboardInterrupt:
    print("\nDone")
    GPIO.cleanup()
    client.disconnect()