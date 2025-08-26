import time
from typing import Callable

import board
import busio
import digitalio
import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

from data import SensorProvider, SensorReading

class HWSensors(SensorProvider):
    sensor_mapping = {
        (0, 0): (0, 0), (0, 1): (0, 1), (0, 2): (0, 2), (0, 3): (0, 3),
        (0, 4): (0, 4), 
    }

    def __init__(self, on_sensor_reading):
        self.on_sensor_reading = on_sensor_reading

        # I2C
        i2c = busio.I2C(board.SCL, board.SDA)
        ads = ADS.ADS1015(i2c)
        # ads.gain = 1
        # ads.data_rate = 1600

        # Channels
        self.channels = [
            AnalogIn(ads, ADS.P0),
            AnalogIn(ads, ADS.P1),
            AnalogIn(ads, ADS.P2),
            AnalogIn(ads, ADS.P3),
        ]

        # Selection
        self.sel_pins = []
        for pin in (board.D5, board.D6, board.D13, board.D19):
            p = digitalio.DigitalInOut(pin)
            p.direction = digitalio.Direction.OUTPUT
            p.value = False
            self.sel_pins.append(p)

    def sensor_reading(self):
        values: SensorReading = {}
        for mul_id in range(16):
            self.set_mux_select(mul_id)
            time.sleep(0.002)

            for adc_id in range(4):
                mapping = self.sensor_mapping[(adc_id, mul_id)]
                values[mapping] = self.channels[adc_id].voltage

        self.on_sensor_reading(values)
        time.sleep(0.25)
    
    def set_mux_select(self, n: int) -> None:
        for bit, p in enumerate(self.sel_pins):
            p.value = bool((n >> bit) & 0x1)

    def set_state(self, state):
        pass