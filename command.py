import paho.mqtt.publish as publish
import time
print("Sending 0...")
publish.single("command", "0", hostname="raspberrypi")
time.sleep(1)
print("Sending 1...")
publish.single("command", "1", hostname="raspberrypi")
