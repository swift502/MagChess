import asyncio

import board
import busio
import digitalio
import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

from chessboard import Chessboard
from data import SensorReading

class HWSensors():
    # ADC input + corresponding multiplexer input
    # Mapped to a chessboard cell coordinate
    sensor_mapping = {
        "a0m00": (0,0), "a1m00": (2,0), "a2m00": (4,0), "a3m00": (6,0),
        "a0m01": (0,1), "a1m01": (2,1), "a2m01": (4,1), "a3m01": (6,1),
        "a0m02": (0,2), "a1m02": (2,2), "a2m02": (4,2), "a3m02": (6,2),
        "a0m03": (0,3), "a1m03": (2,3), "a2m03": (4,3), "a3m03": (6,3),
        "a0m04": (0,4), "a1m04": (2,4), "a2m04": (4,4), "a3m04": (6,4),
        "a0m05": (0,5), "a1m05": (2,5), "a2m05": (4,5), "a3m05": (6,5),
        "a0m06": (0,6), "a1m06": (2,6), "a2m06": (4,6), "a3m06": (6,6),
        "a0m07": (0,7), "a1m07": (2,7), "a2m07": (4,7), "a3m07": (6,7),
        "a0m08": (1,0), "a1m08": (3,0), "a2m08": (5,0), "a3m08": (7,0),
        "a0m09": (1,1), "a1m09": (3,1), "a2m09": (5,1), "a3m09": (7,1),
        "a0m10": (1,2), "a1m10": (3,2), "a2m10": (5,2), "a3m10": (7,2),
        "a0m11": (1,3), "a1m11": (3,3), "a2m11": (5,3), "a3m11": (7,3),
        "a0m12": (1,4), "a1m12": (3,4), "a2m12": (5,4), "a3m12": (7,4),
        "a0m13": (1,5), "a1m13": (3,5), "a2m13": (5,5), "a3m13": (7,5),
        "a0m14": (1,6), "a1m14": (3,6), "a2m14": (5,6), "a3m14": (7,6),
        "a0m15": (1,7), "a1m15": (3,7), "a2m15": (5,7), "a3m15": (7,7),
    }

    def __init__(self, chessboard: Chessboard):
        self.on_sensor_reading = chessboard.update_sensor_values

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

    async def sensor_reading_loop(self):
        while True:
            values: SensorReading = {}
            for mul_id in range(16):
                self.set_aselect(mul_id)
                await asyncio.sleep(0.002)

                for adc_id in range(4):
                    mapping = self.sensor_mapping[f"a{adc_id}m{mul_id:02}"]
                    values[mapping] = self.channels[adc_id].voltage

            self.on_sensor_reading(values)

    def set_aselect(self, n: int) -> None:
        for bit, p in enumerate(self.sel_pins):
            p.value = bool((n >> bit) & 0x1)
