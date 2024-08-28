import serial
import time
from dataclasses import dataclass
from websocket import create_connection
import pandas as pd

@dataclass
class CycleContext:
    cumulative_crank_revs: int = 0
    last_crank_event_time: int = 0
    first_connect: bool = True
    message_sent: bool = False
    cycling_status: str = "stopped"
    measurements: pd.DataFrame = pd.DataFrame(columns=["cumulative_crank_revs", "last_crank_event_time"])
    instant_rpm: pd.DataFrame = pd.DataFrame()
    last_update_time: float = time.time()  # Track the time of the last update

    def update(self, pulse_count: int):
        current_time = time.time()
        if self.cumulative_crank_revs == pulse_count:
            # duplicate event - ignore
            if time.time() - self.last_update_time > 0.35 and self.message_sent:
                print("stopped")
                dist1 = {"status": "stopped"}
                ws1 = create_connection("ws://localhost:7000/websocket")
                ws1.send(str(dist1))
                ws1.close()
                self.message_sent = False
                self.cycling_status = "stopped"
            return
        elif self.cumulative_crank_revs < pulse_count:
            if self.first_connect:
                print("Initial connection established.")
                self.first_connect = False
            else:
                if self.message_sent == False or self.cycling_status == "reverse":
                    self.message_sent = True
                    self.cycling = True
                    print("cycling")
                    dist = {"status": "cycling"}
                    ws = create_connection("ws://localhost:7000/websocket")
                    ws.send(str(dist))
                    ws.close()
                    self.cycling_status = "cycling"
        elif self.cumulative_crank_revs > pulse_count:
            if self.first_connect:
                print("Initial connection established.")
                self.first_connect = False
            else:
                if self.message_sent == False or self.cycling_status == "cycling":
                    self.message_sent = True
                    print("reverse")
                    dist = {"status": "reverse"}
                    ws = create_connection("ws://localhost:7000/websocket")
                    ws.send(str(dist))
                    ws.close()
                    self.cycling_status = "reverse"

        self.cumulative_crank_revs = pulse_count
        self.last_crank_event_time = current_time
        self.last_update_time = current_time

        self.measurements.loc[current_time] = {
            "cumulative_crank_revs": pulse_count,
            "last_crank_event_time": current_time,
        }
        self.diff = self.measurements.diff().tail(-1).ffill()
        self.instant_rpm = (self.diff["cumulative_crank_revs"] / self.diff["last_crank_event_time"] * 60).ffill()
        if not self.instant_rpm.empty:
            self.last_instant_rpm = round(self.instant_rpm.iloc[-1], 2)
            # print(f"Instant RPM: {self.last_instant_rpm}")


def read_serial_data(port: str, baudrate: int = 9600):
    ser = serial.Serial(port, baudrate)
    cycle_context = CycleContext()

    while True:
        if ser.in_waiting > 0:
            try:
                data = ser.readline().decode('utf-8').strip()
                pulse_count = int(data)
                cycle_context.update(pulse_count)
            except ValueError:
                print("Received non-integer data. Ignoring...")
            except Exception as e:
                print(f"Error reading serial data: {e}")  # Small delay to prevent CPU overload


if __name__ == "__main__":
    serial_port = "COM3"  # Replace with your actual serial port
    read_serial_data(serial_port)
