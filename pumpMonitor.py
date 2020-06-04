import time
import paho.mqtt.client as mqtt
import pigpio
# import RPi.GPIO as GPIO
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
FLOAT1 = 21
glitchFilter = 100

pi = pigpio.pi()

pi.set_mode(FLOAT1, pigpio.INPUT)
pi.set_pull_up_down(FLOAT1, pigpio.PUD_DOWN)
pi.set_glitch_filter(FLOAT1, glitchFilter)


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

def levelListener(gpio, level, tick):
    pass


pi.callback(21, pigpio.RISING_EDGE, levelListener)


try:
    while True:
        # if state == operational:
        #     client.publish(TOPIC, 1)
        # elif state == powerOutage:
        #     client.publish(TOPIC, 2)
        # else:
        #     client.publish(TOPIC, 3)


        time.sleep(MAIN_THREAD_DELAY)

except KeyboardInterrupt:
    print("\nDone")
    # GPIO.cleanup()
    client.disconnect()