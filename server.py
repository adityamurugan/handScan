import asyncio
import websockets
import json

CLIENTS = set()
global_flag = False

async def handler(websocket):
    CLIENTS.add(websocket)
    try:
        async for message in websocket:
            parsed_message = parse_message(message)
            if parsed_message:
                broadcast(parsed_message)
    finally:
        CLIENTS.remove(websocket)

async def send(websocket, message):
    try:
        await websocket.send(message)
    except websockets.ConnectionClosed:
        pass

def broadcast(message):
    for websocket in CLIENTS:
        print(message)
        asyncio.create_task(send(websocket, message))

def parse_message(message):
    global global_flag
    try:
        message = message.replace("'", '"')
        data = json.loads(message)
        # Add any additional parsing or validation here
        if 'status' in data:
            if data['status'] == 'cycling':
                global_flag = 'cycling'
            elif data['status'] == 'reverse':
                global_flag = 'reverse'
            else:
                global_flag = 'stopped'
        else:
            if global_flag == 'cycling':
                data['status'] = 'cycling'
            elif global_flag == 'reverse':
                data['status'] = 'reverse'
            else:
                data['status'] = 'stopped'

        return json.dumps(data)  # Convert back to JSON string if needed
    except json.JSONDecodeError:
        print("Failed to decode JSON message")
        return None

async def main():
    async with websockets.serve(handler, "localhost", 7000):
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())