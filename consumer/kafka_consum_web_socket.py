import asyncio
import websockets
import base64
from kafka import KafkaConsumer

# Kafka 설정
kafka_server = "43.201.20.124:9092"
kafka_topic = "coffee" 

# 웹소켓 서버 설정
websocket_clients = set()


# 클라이언트 연결 처리
async def register(websocket):
    websocket_clients.add(websocket)

# 클라이언트 종료 처리
async def unregister(websocket):
    websocket_clients.remove(websocket)


# 웹소켓 서버 핸들러
async def websocket_handler(websocket, path):
    # 클라이언트 호스트 정보 출력
    client_host, client_port = websocket.remote_address
    print(f"Client connected: {client_host}:{client_port}")

    await register(websocket)
    try:
        async for message in websocket:
            # 클라이언트로부터 메시지를 받으면 처리
            pass
    finally:
        await unregister(websocket)
        print(f"Client disconnected: {client_host}:{client_port}")


# Kafka 메시지를 ws 클라이언트에 전달
async def kafka_to_websocket():
    consumer = KafkaConsumer(
        kafka_topic,
        bootstrap_servers=[kafka_server],
        auto_offset_reset="latest",
        group_id="coffee-tree",
    )

    for message in consumer:
        try:
            # 문자열 양끝 "" 제거
            message_str = message.value.decode("utf-8").strip('"')
            # base64 디코딩
            decoded_message = base64.b64decode(message.value).decode("utf-8")
            print(f"Received message: {decoded_message}")
            # 모든 ws 클라이언트에게 메시지 전달
            if websocket_clients: 
                await asyncio.wait(
                    [client.send(decoded_message) for client in websocket_clients]
                )
        except Exception as e:
            print(f"Error: {e}")


async def main():
    websocket_server = await websockets.serve(websocket_handler, "0.0.0.0", 6789)
    await kafka_to_websocket()
    await websocket_server.wait_closed()

asyncio.run(main())
