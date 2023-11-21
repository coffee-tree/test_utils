import paho.mqtt.client as mqtt
import json
import time
import random
import itertools

# MQTT 설정
mqtt_broker = "localhost"
mqtt_port = 1883
mqtt_topic = "coffee"

# 위치 정보
pos = [
    [37.5524, 127.073],
    [37.55222222222222, 127.07326666666665],
    [37.55204444444444, 127.07353333333333],
    [37.55186666666667, 127.07379999999999],
    [37.55168888888889, 127.07406666666667],
    [37.55151111111111, 127.07433333333333],
    [37.55133333333333, 127.0746],
    [37.55115555555556, 127.07486666666667],
    [37.55097777777778, 127.07513333333334],
    [37.5508, 127.0754],
    [37.5508, 127.0754],
    [37.5506, 127.07534444444444],
    [37.5504, 127.07528888888889],
    [37.550200000000004, 127.07523333333333],
    [37.550000000000004, 127.07517777777778],
    [37.5498, 127.07512222222222],
    [37.5496, 127.07506666666667],
    [37.5494, 127.07501111111111],
    [37.5492, 127.07495555555556],
    [37.549, 127.0749],
    [37.549, 127.0749],
    [37.54915555555556, 127.07471111111111],
    [37.54931111111111, 127.07452222222223],
    [37.54946666666667, 127.07433333333333],
    [37.549622222222226, 127.07414444444444],
    [37.54977777777778, 127.07395555555556],
    [37.549933333333335, 127.07376666666667],
    [37.550088888888894, 127.07357777777777],
    [37.550244444444445, 127.07338888888889],
    [37.5504, 127.0732],
    [37.5504, 127.0732],
    [37.55062222222222, 127.07317777777777],
    [37.550844444444444, 127.07315555555556],
    [37.55106666666667, 127.07313333333333],
    [37.55128888888889, 127.0731111111111],
    [37.55151111111111, 127.07308888888889],
    [37.55173333333333, 127.07306666666666],
    [37.55195555555556, 127.07304444444443],
    [37.55217777777778, 127.07302222222222],
    [37.5524, 127.073],
    [37.5524, 127.073],
]

last_message = None # 최근 발행 메시지

count = 10;
status = "Active" # 기본 상태

# 콜백함수
def on_publish(client, userdata, mid):
    print(f"Message published with mid: {mid}")
    if last_message is not None:
        print(f"Published message: {last_message}")


# MQTT 클라이언트
producer_client = mqtt.Client()

# 콜백 함수 설정
producer_client.on_publish = on_publish

# MQTT 브로커와 연결
producer_client.connect(mqtt_broker, mqtt_port, 60)

# pos 반복
for x, y in itertools.cycle(pos):
    data = {"id": "3DF92-192", "x": x, "y": y, "status": status}

    # JSON 데이터 직렬화해서 발행
    message = json.dumps(data)
    last_message = message
    (rc, mid) = producer_client.publish(mqtt_topic, message.encode("utf-8"))
    # 비활성화 상태일 때 메시지 추가 전송 잠자기
    if status == "Inactive":
        (rc, mid) = producer_client.publish(mqtt_topic, message.encode("utf-8"))
        (rc, mid) = producer_client.publish(mqtt_topic, message.encode("utf-8"))
        (rc, mid) = producer_client.publish(mqtt_topic, message.encode("utf-8"))
        (rc, mid) = producer_client.publish(mqtt_topic, message.encode("utf-8"))
        (rc, mid) = producer_client.publish(mqtt_topic, message.encode("utf-8"))
        status = "Active"
        time.sleep(15)
    if rc != mqtt.MQTT_ERR_SUCCESS:
        print(f"Failed to publish message. Return code: {rc}")

    # 특정 횟수 이후 비활성화 상태로 만들기
    count-=1
    if count == 1 :
        status = "Inactive"
        count = 10
    sleep_time = random.randint(4, 6)
    time.sleep(sleep_time)