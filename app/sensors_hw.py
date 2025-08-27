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
        "mux_0_00": (0,0), "mux_1_00": (2,0), "mux_2_00": (4,0), "mux_3_00": (6,0),
        "mux_0_01": (0,1), "mux_1_01": (2,1), "mux_2_01": (4,1), "mux_3_01": (6,1),
        "mux_0_02": (0,2), "mux_1_02": (2,2), "mux_2_02": (4,2), "mux_3_02": (6,2),
        "mux_0_03": (0,3), "mux_1_03": (2,3), "mux_2_03": (4,3), "mux_3_03": (6,3),
        "mux_0_04": (0,4), "mux_1_04": (2,4), "mux_2_04": (4,4), "mux_3_04": (6,4),
        "mux_0_05": (0,5), "mux_1_05": (2,5), "mux_2_05": (4,5), "mux_3_05": (6,5),
        "mux_0_06": (0,6), "mux_1_06": (2,6), "mux_2_06": (4,6), "mux_3_06": (6,6),
        "mux_0_07": (0,7), "mux_1_07": (2,7), "mux_2_07": (4,7), "mux_3_07": (6,7),
        "mux_0_08": (1,0), "mux_1_08": (3,0), "mux_2_08": (5,0), "mux_3_08": (7,0),
        "mux_0_09": (1,1), "mux_1_09": (3,1), "mux_2_09": (5,1), "mux_3_09": (7,1),
        "mux_0_10": (1,2), "mux_1_10": (3,2), "mux_2_10": (5,2), "mux_3_10": (7,2),
        "mux_0_11": (1,3), "mux_1_11": (3,3), "mux_2_11": (5,3), "mux_3_11": (7,3),
        "mux_0_12": (1,4), "mux_1_12": (3,4), "mux_2_12": (5,4), "mux_3_12": (7,4),
        "mux_0_13": (1,5), "mux_1_13": (3,5), "mux_2_13": (5,5), "mux_3_13": (7,5),
        "mux_0_14": (1,6), "mux_1_14": (3,6), "mux_2_14": (5,6), "mux_3_14": (7,6),
        "mux_0_15": (1,7), "mux_1_15": (3,7), "mux_2_15": (5,7), "mux_3_15": (7,7),
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
                    mapping = self.sensor_mapping[f"mux_{adc_id}_{mul_id:02}"]
                    values[mapping] = self.channels[adc_id].voltage

            self.on_sensor_reading(values)
            await asyncio.sleep(1/30)

    def set_mux_select(self, n: int) -> None:
        for bit, p in enumerate(self.sel_pins):
            p.value = bool((n >> bit) & 0x1)
