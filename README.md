# test_utils

# MQTT 메시지 발행하기

> Kafka를 통한 메시지 전달과정은 아래와 같다  
> `MQTT publisher` -> `MQTT broker` -> `Kafka Connector` -> `Kafka broker` -> `Kafka Consumer`  
> `MQTT broker`는 `Kafka Producer`이기도 하다.

## MQTT Publisher

> publisher 를 flask를 통해 웹 서버로 배포한다.
> publishing 은 다른 스레드에서 백그라운드로 진행되며,  
> REST api를 통해 device id의 status를 관리한다.

#### status 변경을 위한 page에 route

```py
@app.route('/')
def index():
    return render_template('index.html',
                           status_3DF92_192=status_dict["3DF92-192"],
                           status_4HHC2_392=status_dict["4HHC2-392"])
```

#### MQTT 설정 정보

```py
mqtt_broker = "localhost"
mqtt_port = 1883
mqtt_topic = "coffee"
```

오해하면 안 되는 부분이 해당 코드는 `mqtt 브로커`에게 전달 되는 `mqtt 메시지`를 발행하는 것이다. `mqtt_topic = "coffee"`는 `mqtt 브로커`와 통신할 때 구분할 수 있는 topic이다.

#### device status 관리 정보

```py

# 초기 상태
status_dict = {
"3DF92-192": "Active",
"4HHC2-392": "Active"
}

# 최근 상태
last_status_dict = {
"3DF92-192": "Active",
"4HHC2-392": "Active"
}
```

### MQTT 프로듀서 함수

#### mqtt 브로커와 연결

```py
producer_client = mqtt.Client()
producer_client.connect(mqtt_broker, mqtt_port, 60)
```

#### mqtt 브로커에 메시지를 발행

```py
if current_status == "Active":
            x, y = pos[pos_index]
            data = {"id": device_id, "x": x, "y": y, "status": current_status}
            message = json.dumps(data)
            producer_client.publish(mqtt_topic, message.encode("utf-8"))
            pos_index = (pos_index + 1) % len(pos)

            sleep_time = random.randint(1, 2)
            time.sleep(sleep_time)
        else:
            time.sleep(1)
```

Active일 때는 메시지를 발행하고, Inactive일때는 대기하도록한다.

퍼블리싱은 `producer_client.publish(mqtt_topic, message.encode("utf-8"))` 해당 코드에서 이루어진다.

Inactive가 되는 순간 최초 1회 메시지가 발행되도록 코드를 추가한다.

```py
if current_status == "Inactive" and last_status == "Active":
            x, y = pos[pos_index]
            data = {"id": device_id, "x": x, "y": y, "status": current_status}
            message = json.dumps(data)
            producer_client.publish(mqtt_topic, message.encode("utf-8"))
```

status가 Inactive로 변경된 순간 메시지를 하나 발생 시킨다

#### mqtt_producer 함수 전체

```py
def mqtt_producer(device_id):
producer_client = mqtt.Client()
producer_client.connect(mqtt_broker, mqtt_port, 60)

    pos_index = 0
    while True:
        current_status = status_dict[device_id]
        last_status = last_status_dict[device_id]

        if current_status == "Inactive" and last_status == "Active":
            x, y = pos[pos_index]
            data = {"id": device_id, "x": x, "y": y, "status": current_status}
            message = json.dumps(data)
            producer_client.publish(mqtt_topic, message.encode("utf-8"))

        if current_status == "Active":
            x, y = pos[pos_index]
            data = {"id": device_id, "x": x, "y": y, "status": current_status}
            message = json.dumps(data)
            producer_client.publish(mqtt_topic, message.encode("utf-8"))
            pos_index = (pos_index + 1) % len(pos)

            sleep_time = random.randint(1, 2)
            time.sleep(sleep_time)
        else:
            time.sleep(1)

        last_status_dict[device_id] = current_status
```

### rest api 처리

#### index.html

```py
@app.route('/')
def index():
    return render_template('index.html',
    status_3DF92_192=status_dict["3DF92-192"],
    status_4HHC2_392=status_dict["4HHC2-392"])
```

flask의 render_template기능을 활용하여 divec_id의 현재 status를 html에 바인딩한다.

#### status 변경 POST 처리

```py
@app.route('/status/<device_id>', methods=['POST'])
def update_status(device_id):
    data = request.get_json()
    if 'status' in data and data['status'] in ["Active", "Inactive"]:
        status_dict[device_id] = data['status']
        return jsonify({"message": f"Status of {device_id} updated to {data['status']}"}), 200
    else:
        return jsonify({"message": "Invalid status"}), 400
```

post 바디에 있는 status 값을 받아 해당 uri device_id에 반영한다.

### server 실행

```
producer_thread1 = threading.Thread(target=mqtt_producer, args=("3DF92-192",))
producer_thread2 = threading.Thread(target=mqtt_producer, args=("4HHC2-392",))
producer_thread1.start()
producer_thread2.start()

```

## MQTT broker

### MQTT broker 설치 및 실행

```
sudo apt-get install mosquitto mosquitto-clients
sudo systemctl start mosquitto
```

`mosquitto`를 실행시키면 기본적으로 1883 port에 mqtt broker가 실행된다.
추가적인 코드 설정은 필요없으며, producer에서 topic을 지정해서 발행하면 알아서 처리해준다.
