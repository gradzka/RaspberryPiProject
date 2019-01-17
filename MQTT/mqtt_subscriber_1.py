import paho.mqtt.client as mqttClient
import time

diode_state = 1


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("S1: Connected to broker")
        global Connected  # Use global variable
        Connected = True  # Signal connection
        client.subscribe('paho/button_state')
    else:
        print("Connection failed")


def on_message(client, userdata, message):
    if (int(message.payload)) == 1:
        print("BUTTON NOT PRESSED")
    else:
        print("BUTTON PRESSED")


Connected = False  # global variable for the state of the connection
broker_address = "192.168.1.104"  # Broker address
port = 1883  # Broker port
client = mqttClient.Client("S1")  # create new instance
client.on_connect = on_connect  # attach function to callback
client.on_message = on_message  # attach function to callback
client.connect(broker_address, port=port)  # connect to broker
client.loop_start()  # start the loop

while Connected is not True:  # Wait for connection
    time.sleep(0.1)

while True:
    time.sleep(1)
    diode_state = not diode_state
    if diode_state is False:
        client.publish("paho/toggle_diode", "0")
    else:
        client.publish("paho/toggle_diode", "1")