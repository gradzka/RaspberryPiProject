import paho.mqtt.client as mqttClient
import time
import wiringpi


wiringpi.wiringPiSetupGpio()  # For GPIO pin numbering
wiringpi.pinMode(13, wiringpi.OUTPUT)
wiringpi.digitalWrite(13, wiringpi.LOW)
wiringpi.pinMode(13, wiringpi.INPUT)
wiringpi.pullUpDnControl(13, wiringpi.GPIO.PUD_UP)


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("S2: Connected to broker")
        global Connected  # Use global variable
        Connected = True  # Signal connection
        client.subscribe('paho/toggle_diode')
    else:
        print("Connection failed")


def on_message(client, userdata, message):
    toggle_diode(int(message.payload))


def toggle_diode(diode_state):
    wiringpi.pinMode(26, diode_state)  # Set pin 26 to 1 ( OUTPUT )
    wiringpi.digitalWrite(26, diode_state)  # Write 1 ( HIGH ) to pin 6


Connected = False  # global variable for the state of the connection
broker_address = "192.168.1.104"  # Broker address
port = 1883  # Broker port
client = mqttClient.Client("S2")  # create new instance
client.on_connect = on_connect  # attach function to callback
client.on_message = on_message  # attach function to callback
client.connect(broker_address, port=port)  # connect to broker
client.loop_start()  # start the loop

while Connected is not True:  # Wait for connection
    time.sleep(0.1)

while True:
    time.sleep(1)
    client.publish("paho/button_state", wiringpi.digitalRead(13))
