from random import randint

from constants import SENSOR_THRESHOLD_HIGH, SENSOR_THRESHOLD_LOW

class SensorProvider:
    def get_value_array(self) -> dict[tuple[int, int], float]:
        raise NotImplementedError()
    
class HWSensors(SensorProvider):
    def __init__(self):
        raise NotImplementedError()

    def get_value_array(self):
        raise NotImplementedError()

class SWSensorObject:
    signal_strength = 500
    noise = 100

    def __init__(self, state: int):
        self.state = state

    def get_value(self):
        if self.state == 1:
            return randint(SENSOR_THRESHOLD_HIGH - self.noise, SENSOR_THRESHOLD_HIGH + self.signal_strength)
        elif self.state == -1:
            return randint(SENSOR_THRESHOLD_LOW - self.signal_strength, SENSOR_THRESHOLD_LOW + self.noise)
        else: # if self.state == 0:
            return randint(SENSOR_THRESHOLD_LOW - self.noise, SENSOR_THRESHOLD_HIGH + self.noise)

    def set_state(self, state):
        self.state = state

class SWSensors (SensorProvider):
    sensors: dict[tuple[int, int], SWSensorObject]

    def __init__(self):
        self.sensors = {}

        for letter in range(8):
            for number in range(8):
                state = 0
                if letter == 0 or letter == 1:
                    state = 1
                if letter == 6 or letter == 7:
                    state = -1
                self.sensors[(letter, number)] = SWSensorObject(state)

    def get_value_array(self):
        values: dict[tuple[int, int], float] = {}
        for key, sensor in self.sensors.items():
            values[key] = float(sensor.get_value())
        return values