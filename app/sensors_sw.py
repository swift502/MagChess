import asyncio
import random
from typing import Callable

from constants import SENSOR_CALIBRATION_DATA, SENSOR_TRIGGER_DELTA, SENSOR_SIM_NOISE

class SWSensorObject:
    def __init__(self, coords: tuple[int, int], state: int):
        self.ref_value = SENSOR_CALIBRATION_DATA[str(coords)]
        self.state = state

    def get_value(self):
        if self.state == 1:
            return self.ref_value - 2 * SENSOR_TRIGGER_DELTA + self.get_noise()
        elif self.state == 3:
            return self.ref_value + 2 * SENSOR_TRIGGER_DELTA + self.get_noise()
        else:
            return self.ref_value + self.get_noise()

    def get_noise(self):
        return random.randint(-SENSOR_SIM_NOISE, SENSOR_SIM_NOISE)

    def set_state(self, state: int):
        self.state = state

class SWSensors():
    sensors: dict[tuple[int, int], SWSensorObject]

    def __init__(self, on_sensor_reading: Callable[[tuple[int, int], int], None], flipped: bool = False):
        self.sensors = {}
        self.on_sensor_reading = on_sensor_reading

        for co_letter in range(8):
            for co_number in range(8):
                coords = (co_letter, co_number)
                state = 0
                if co_number == 0 or co_number == 1:
                    state = 3 if flipped else 1
                if co_number == 6 or co_number == 7:
                    state = 1 if flipped else 3
                self.sensors[coords] = SWSensorObject(coords, state)

    async def sensor_reading_loop(self):
        while True:
            for key, sensor in self.sensors.items():
                self.on_sensor_reading(key, sensor.get_value())

            await asyncio.sleep(1/6)

    def on_sensor_click(self, co_letter: int, co_number: int):
        state = self.sensors[(co_letter, co_number)].state
        state += 1
        if state == 4:
            state = 0
        self.sensors[(co_letter, co_number)].set_state(state)