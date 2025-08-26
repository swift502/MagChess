import asyncio

import board
import busio
import digitalio
import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

from chessboard import Chessboard
from data import SensorReading

class HWSensors():
    sensor_mapping = {
         "a0m0":(0,0),  "a1m0":(0,1),  "a2m0":(0,2),  "a3m0":(0,3),
         "a0m1":(0,4),  "a1m1":(0,5),  "a2m1":(0,6),  "a3m1":(0,7),
         "a0m2":(1,0),  "a1m2":(1,1),  "a2m2":(1,2),  "a3m2":(1,3),
         "a0m3":(1,4),  "a1m3":(1,5),  "a2m3":(1,6),  "a3m3":(1,7),
         "a0m4":(2,0),  "a1m4":(2,1),  "a2m4":(2,2),  "a3m4":(2,3),
         "a0m5":(2,4),  "a1m5":(2,5),  "a2m5":(2,6),  "a3m5":(2,7),
         "a0m6":(3,0),  "a1m6":(3,1),  "a2m6":(3,2),  "a3m6":(3,3),
         "a0m7":(3,4),  "a1m7":(3,5),  "a2m7":(3,6),  "a3m7":(3,7),
         "a0m8":(4,0),  "a1m8":(4,1),  "a2m8":(4,2),  "a3m8":(4,3),
         "a0m9":(4,4),  "a1m9":(4,5),  "a2m9":(4,6),  "a3m9":(4,7),
        "a0m10":(5,0), "a1m10":(5,1), "a2m10":(5,2), "a3m10":(5,3),
        "a0m11":(5,4), "a1m11":(5,5), "a2m11":(5,6), "a3m11":(5,7),
        "a0m12":(6,0), "a1m12":(6,1), "a2m12":(6,2), "a3m12":(6,3),
        "a0m13":(6,4), "a1m13":(6,5), "a2m13":(6,6), "a3m13":(6,7),
        "a0m14":(7,0), "a1m14":(7,1), "a2m14":(7,2), "a3m14":(7,3),
        "a0m15":(7,4), "a1m15":(7,5), "a2m15":(7,6), "a3m15":(7,7),
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
                self.set_mux_select(mul_id)
                await asyncio.sleep(0.002)

                for adc_id in range(4):
                    mapping = self.sensor_mapping[f"a{adc_id}m{mul_id}"]
                    values[mapping] = self.channels[adc_id].voltage

            self.on_sensor_reading(values)
            await asyncio.sleep(1/30)

    def set_mux_select(self, n: int) -> None:
        for bit, p in enumerate(self.sel_pins):
            p.value = bool((n >> bit) & 0x1)
