from kafka import KafkaConsumer
import base64

kafka_server = "43.201.20.124:9092"
kafka_topic = "coffee"

consumer = KafkaConsumer(
    kafka_topic,
    bootstrap_servers=[kafka_server],
    auto_offset_reset="latest",
    group_id="coffee-tree",
)

print(f"Listening for messages on topic '{kafka_topic}'...")
for message in consumer:
    try:
        decoded_message = base64.b64decode(message.value).decode("utf-8")
        print(f"Received message: {decoded_message}")
    except Exception as e:
        print(f"Error decoding message: {e}")
