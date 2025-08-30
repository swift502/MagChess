import asyncio
from random import randint

from chessboard import Chessboard
from constants import SENSOR_THRESHOLD_HIGH, SENSOR_THRESHOLD_LOW
from data import SensorReading

class SWSensorObject:
    signal_strength = 500
    noise = 100

    def __init__(self, state: int):
        self.state = state

    def get_value(self):
        if self.state == 2:
            return randint(SENSOR_THRESHOLD_LOW - self.signal_strength, SENSOR_THRESHOLD_LOW + self.noise)
        elif self.state == 0:
            return randint(SENSOR_THRESHOLD_HIGH - self.noise, SENSOR_THRESHOLD_HIGH + self.signal_strength)
        else:
            return randint(SENSOR_THRESHOLD_LOW - self.noise, SENSOR_THRESHOLD_HIGH + self.noise)

    def set_state(self, state: int):
        self.state = state

class SWSensors():
    sensors: dict[tuple[int, int], SWSensorObject]

    def __init__(self, chessboard: Chessboard, flipped: bool):
        self.sensors = {}
        self.on_sensor_reading = chessboard.update_sensor_values

        for co_letter in range(8):
            for co_number in range(8):
                state = 1
                if co_number == 0 or co_number == 1:
                    state = 0 if flipped else 2
                if co_number == 6 or co_number == 7:
                    state = 2 if flipped else 0
                self.sensors[(co_letter, co_number)] = SWSensorObject(state)

    async def sensor_reading_loop(self):
        values: SensorReading  = {}
        
        while True:
            for key, sensor in self.sensors.items():
                values[key] = float(sensor.get_value())

            self.on_sensor_reading(values)
            await asyncio.sleep(1/30)

    def on_sensor_click(self, co_letter: int, co_number: int):
        state = self.sensors[(co_letter, co_number)].state
        state += 1
        if state == 4:
            state = 0
        self.sensors[(co_letter, co_number)].set_state(state)