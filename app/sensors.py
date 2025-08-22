from random import randint

class SensorProvider:
    def get_value_array(self) -> dict[tuple[int, int], float]:
        raise NotImplementedError()
    
class HWSensors(SensorProvider):
    def __init__(self):
        raise NotImplementedError()

    def get_value_array(self):
        raise NotImplementedError()

class SWSensorObject:
    low_border = 32500
    high_border = 33000
    signal_strength = 500
    noise = 200

    def __init__(self, state: int):
        self.state = state

    def get_value(self):
        if self.state == -1:
            return randint(self.low_border - self.signal_strength, self.low_border + self.noise)
        elif self.state == 0:
            return randint(self.low_border - self.noise, self.high_border + self.noise)
        elif self.state == 1:
            return randint(self.high_border - self.noise, self.high_border + self.signal_strength)

    def set_state(self, state):
        self.state = state

class SWSensors (SensorProvider):
    sensors: dict[tuple[int, int], SWSensorObject]

    def __init__(self, emulator: bool):
        self.sensors = {}

        if emulator:
            for letter in range(8):
                for number in range(8):
                    state = 0
                    if letter == 0 or letter == 1:
                        state = 1
                    if letter == 6 or letter == 7:
                        state = -1
                    self.sensors[(letter, number)] = SWSensorObject(state)

    def get_value_array(self):
        values = {}
        for key, sensor in self.sensors.items():
            values[key] = sensor.get_value()
        return values