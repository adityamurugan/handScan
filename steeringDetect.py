import asyncio
from bleak import BleakClient

from pycycling.sterzo import Sterzo
from websocket import create_connection


async def run(address):
    async with BleakClient(address) as client:
        def steering_handler(steering_angle):
            print(steering_angle)
            if steering_angle>0:
                steering_angle_norm = steering_angle/37
            elif steering_angle<0:
                steering_angle_norm = steering_angle/32
            else:
                steering_angle_norm = steering_angle
            dist = {"steer":round(steering_angle_norm,7)}
            ws = create_connection("ws://localhost:7000/websocket")
            ws.send(str(dist))
            ws.close()

        await client.is_connected()
        sterzo = Sterzo(client)
        sterzo.set_steering_measurement_callback(steering_handler)
        await sterzo.enable_steering_measurement_notifications()
        await asyncio.sleep(300)

if __name__ == "__main__":
    import os

    os.environ["PYTHONASYNCIODEBUG"] = str(1)

    device_address = "C8:0A:8D:D1:B8:28"
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run(device_address))