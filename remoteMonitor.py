import time
import paho.mqtt.client as mqtt
# import RPi.GPIO as GPIO

BROKER = 'iot.cs.calvin.edu'
USERNAME = "cs300" # Put broker username here
PASSWORD = "safeIoT"
TOPIC = 'chris/pump'
CERTS = '/etc/ssl/certs/ca-certificates.crt'
PORT = 8883
QOS = 0

MAIN_THREAD_DELAY = 10

operational = 1
powerOutage = 2
internetOutage = 3

state = operational
stateList = [operational, powerOutage, internetOutage]


# Callback when client receives a PUBLISH message from the broker
def on_message(client, data, msg):
    if msg.topic == TOPIC:
        message = int(msg.payload)
        print("Received message: LED = ", message)

        if message == operational:
            pass
            #set lights
        elif message == powerOutage:
            pass
            #set lights
        else:
            # sendEmail()

        
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


