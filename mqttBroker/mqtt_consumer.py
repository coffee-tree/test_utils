import paho.mqtt.client as mqtt

mqtt_broker = "localhost"
mqtt_port = 1883
mqtt_topic = "coord"

def on_message(client, userdata, message):
    print(f"Received message: {message.payload.decode()}")

consumer_client = mqtt.ClientW()

consumer_client.on_message = on_message

consumer_client.connect(mqtt_broker, mqtt_port, 60)

consumer_client.subscribe(mqtt_topic)

consumer_client.loop_forever()
