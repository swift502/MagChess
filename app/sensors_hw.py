import asyncio
from typing import Callable
import board
import busio
import digitalio
import adafruit_ads1x15.ads1015 as ADS
# from adafruit_ads1x15.ads1x15 import Mode
from adafruit_ads1x15.analog_in import AnalogIn

from ui_instance import MagChessUI

class HWSensors():
    # ADC input + corresponding multiplexer input
    # Mapped to a chessboard cell coordinate
    sensor_mapping = {
        "a0m00": (4,1), "a1m00": (7,6), "a2m00": (0,1), "a3m00": (3,6),
        "a0m01": (4,2), "a1m01": (7,5), "a2m01": (0,2), "a3m01": (3,5),
        "a0m02": (4,3), "a1m02": (7,4), "a2m02": (0,3), "a3m02": (3,4),
        "a0m03": (5,3), "a1m03": (6,4), "a2m03": (1,3), "a3m03": (2,4),
        "a0m04": (5,2), "a1m04": (6,5), "a2m04": (1,2), "a3m04": (2,5),
        "a0m05": (5,1), "a1m05": (6,6), "a2m05": (1,1), "a3m05": (2,6),
        "a0m06": (4,0), "a1m06": (7,7), "a2m06": (0,0), "a3m06": (3,7),
        "a0m07": (5,0), "a1m07": (6,7), "a2m07": (1,0), "a3m07": (2,7),
        "a0m08": (6,0), "a1m08": (5,7), "a2m08": (2,0), "a3m08": (1,7),
        "a0m09": (7,0), "a1m09": (4,7), "a2m09": (3,0), "a3m09": (0,7),
        "a0m10": (6,1), "a1m10": (5,6), "a2m10": (2,1), "a3m10": (1,6),
        "a0m11": (6,2), "a1m11": (5,5), "a2m11": (2,2), "a3m11": (1,5),
        "a0m12": (6,3), "a1m12": (5,4), "a2m12": (2,3), "a3m12": (1,4),
        "a0m13": (7,3), "a1m13": (4,4), "a2m13": (3,3), "a3m13": (0,4),
        "a0m14": (7,2), "a1m14": (4,5), "a2m14": (3,2), "a3m14": (0,5),
        "a0m15": (7,1), "a1m15": (4,6), "a2m15": (3,1), "a3m15": (0,6),
    }

    init_fail: bool = False

    def __init__(self, on_sensor_reading: Callable[[tuple[int, int], int], None], ui: MagChessUI | None = None):
        self.on_sensor_reading = on_sensor_reading

        # I2C
        try:
            i2c = busio.I2C(board.SCL, board.SDA)
            ads = ADS.ADS1015(i2c)
            #ads.mode = Mode.CONTINUOUS
            ads.data_rate = 3300
        except ValueError:
            if ui:
                ui.display_error("Chessboard connection not found.")
            self.init_fail = True
            return

        # Channels
        self.channels = [
            AnalogIn(ads, ADS.P0),
            AnalogIn(ads, ADS.P1),
            AnalogIn(ads, ADS.P2),
            AnalogIn(ads, ADS.P3),
        ]

        # Selection
        self.sel_pins = []
        for pin in (board.D21, board.D20, board.D16, board.D12):
            p = digitalio.DigitalInOut(pin)
            p.direction = digitalio.Direction.OUTPUT
            p.value = False
            self.sel_pins.append(p)

    async def sensor_reading_loop(self):
        if self.init_fail:
            return

        while True:
            for mul_id in range(16):
                self.set_aselect(mul_id)
                await asyncio.sleep(0.001)

                for adc_id in range(4):
                    mapping = self.sensor_mapping[f"a{adc_id}m{mul_id:02}"]
                    self.on_sensor_reading(mapping, self.channels[adc_id].value)

    def set_aselect(self, n: int) -> None:
        for bit, p in enumerate(self.sel_pins):
            p.value = bool((n >> bit) & 0x1)
