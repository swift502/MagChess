from random import randint

from constants import SENSOR_THRESHOLD_HIGH, SENSOR_THRESHOLD_LOW
from data import SensorProvider

class SWSensorObject:
    signal_strength = 500
    noise = 100

    def __init__(self, state: int):
        self.state = state

    def get_value(self):
        if self.state == 0:
            return randint(SENSOR_THRESHOLD_LOW - self.signal_strength, SENSOR_THRESHOLD_LOW + self.noise)
        elif self.state == 2:
            return randint(SENSOR_THRESHOLD_HIGH - self.noise, SENSOR_THRESHOLD_HIGH + self.signal_strength)
        else:
            return randint(SENSOR_THRESHOLD_LOW - self.noise, SENSOR_THRESHOLD_HIGH + self.noise)

    def set_state(self, state):
        self.state = state

class SWSensors(SensorProvider):
    sensors: dict[tuple[int, int], SWSensorObject]

    def __init__(self):
        self.sensors = {}

        for co_letter in range(8):
            for co_number in range(8):
                state = 1
                if co_number == 0 or co_number == 1:
                    state = 2
                if co_number == 6 or co_number == 7:
                    state = 0
                self.sensors[(co_letter, co_number)] = SWSensorObject(state)

    def get_value_array(self):
        values: dict[tuple[int, int], float] = {}
        for key, sensor in self.sensors.items():
            values[key] = float(sensor.get_value())
        return values

    def cycle_sensor_state(self, co_letter: int, co_number: int):
        state = self.sensors[(co_letter, co_number)].state
        state += 1
        if state == 4:
            state = 0
        self.sensors[(co_letter, co_number)].set_state(state)