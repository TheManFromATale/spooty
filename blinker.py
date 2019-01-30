import paho.mqtt.client as m_client
import time
import RPi.GPIO as GPIO

def off():
    GPIO.output(13, GPIO.HIGH)
    GPIO.output(19, GPIO.HIGH)
    GPIO.output(26, GPIO.HIGH)
    GPIO.output(6, GPIO.HIGH)


def callback(client, userdata, message):
    decoded = str(message.payload.decode('utf-8'))
    print("message recieved: {}".format(decoded))
    if decoded is "r":
        off()
        for n in range(3):
            GPIO.output(26, GPIO.LOW)
            GPIO.output(19, GPIO.LOW)
            time.sleep(0.5)
            off()
            time.sleep(1)
    elif decoded is "l":
        off()
        for n in range(3):
            GPIO.output(13, GPIO.LOW)
            GPIO.output(6, GPIO.LOW)
            time.sleep(0.5)
            off()
            time.sleep(1)
    elif decoded is "0": 
        off()


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(26, GPIO.OUT) #26,29
GPIO.setup(19, GPIO.OUT)
GPIO.setup(6, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)
off()
client = m_client.Client("P1")
client.on_message = callback

client.connect("127.0.0.1")
client.subscribe("blinker")

while True:
    client.loop_start()
    time.sleep(0.25)
