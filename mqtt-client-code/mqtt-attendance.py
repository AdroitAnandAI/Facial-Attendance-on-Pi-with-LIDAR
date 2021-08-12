#!/usr/bin/env python3

import paho.mqtt.client as mqtt
import data_manage as dm

# This is the Subscriber

conn = dm.create_connection(r"attendance.db")

count = 0


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("safetycam/topic/register")


def on_message(client, userdata, msg):
    # print("Received Message...")

    word = msg.payload.decode()
    attributes = word.split('|')
    dm.insert_attendance(conn, tuple(attributes))
    count = count + 1


client = mqtt.Client()
client.connect("test.mosquitto.org", 1883, 600)

client.on_connect = on_connect
client.on_message = on_message

try:
    client.loop_forever()
# Catches SigINT
except KeyboardInterrupt:
    client.disconnect()
