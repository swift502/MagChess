from random import random

class Sensor:
    def get_value(self):
        pass
    
class SensorSS49E(Sensor):
    def __init__(self, pin):
        self.pin = pin

    def get_value(self):
        pass

class SensorSW(Sensor):

    state: int

    low_border = 32500
    high_border = 33000
    signal_strength = 500
    noise = 200

    def get_value(self):
        if self.state == -1:
            return random.randint(self.low_border - self.signal_strength, self.low_border + self.noise)
        elif self.state == 0:
            return random.randint(self.low_border - self.noise, self.high_border + self.noise)
        elif self.state == 1:
            return random.randint(self.high_border - self.noise, self.high_border + self.signal_strength)

    def set_state(self, state):
        self.state = state

class Sensors:

    sensors: dict[tuple[int, int], Sensor]

    def __init__(self, emulator: bool):
        if emulator:
            for x in range(8):
                for y in range(8):
                    self.sensors[(x, y)] = SensorSW()
        else:
            # TODO
            pass
