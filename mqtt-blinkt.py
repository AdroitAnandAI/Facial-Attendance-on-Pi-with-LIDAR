#!/usr/bin/env python
import time
from sys import exit

import sendsms

try:
    import paho.mqtt.client as mqtt
except ImportError:
    exit("This example requires the paho-mqtt module\nInstall with: sudo pip install paho-mqtt")

import blinkt


MQTT_SERVER = "test.mosquitto.org"
MQTT_PORT = 1883
MQTT_TOPIC = "safetycam/topic/blinkt"

# Set these to use authorisation
MQTT_USER = None
MQTT_PASS = None

# To give color to the light show - red for unknown, green for known
REDS = [0, 0, 0, 0, 0, 16, 64, 255, 64, 16, 0, 0, 0, 0, 0, 0]

print("""
MQTT Blinkt! Control

This program monitors public MQTT messages from {server} on port {port} to control Blinkt!

It will monitor the {topic} topic by default. The blinkt will flash red for 'no entry' and send sms

The blink will flash green in case the person is identified, to signify door open event.
""".format(
    server=MQTT_SERVER,
    port=MQTT_PORT,
    topic=MQTT_TOPIC
))

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    client.subscribe(MQTT_TOPIC)

def on_message(client, userdata, msg):

    # print("on message")
    data = msg.payload.decode()

    # Enable SMS only for final video recording
    if (data == 'red'):
        sendsms.informSecurity()

    start_time = time.time()

    for _ in range(30):

       # The light will flash red when the person is not identified
       # and green when the person is identified. Signifies Door Opening.
       delta = (time.time() - start_time) * 16
       offset = int(abs((delta % len(REDS)) - blinkt.NUM_PIXELS))

       for i in range(blinkt.NUM_PIXELS):
           if (data == 'red'):
               blinkt.set_pixel(i , REDS[offset + i], 0, 0)
           else:
               blinkt.set_pixel(i , 0, REDS[offset + i], 0)

       blinkt.show()
       time.sleep(0.1)

    blinkt.clear()
    blinkt.show()

    return


blinkt.set_clear_on_exit()

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

if MQTT_USER is not None and MQTT_PASS is not None:
    print("Using username: {un} and password: {pw}".format(un=MQTT_USER, pw="*" * len(MQTT_PASS)))
    client.username_pw_set(username=MQTT_USER, password=MQTT_PASS)

client.connect(MQTT_SERVER, MQTT_PORT, 600)

client.loop_forever()