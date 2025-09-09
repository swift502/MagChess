import argparse
import asyncio
import json
import sys
import time

from sensors_hw import HWSensors
from utilities import data_path

sensor_count = 64
sample_count = sensor_count * 10
samples: dict[tuple[int, int], list[int]] = {}

time_samples: list[float] = []
last_time: float | None = None
counter: int = 0

def export_calibration_data():
    average = {str(coords): sum(samples[coords]) // len(samples[coords]) for coords in samples}
    average = dict(sorted(average.items()))
    path = data_path("sensor_calibration_data.json")
    with open(path, "w") as f:
        json.dump(average, f, indent=4)

    print(f'Written "{path}"')

def on_sensor_reading(coords: tuple[int, int], value: int, write: bool):
    if coords not in samples:
        samples[coords] = []
    samples[coords].append(value)

    global counter
    counter += 1
    if counter % sensor_count == 0:
        global time_samples, last_time
        print(f"\rSampled {counter}/{sample_count}", end="")
        now = time.perf_counter()
        if last_time is not None:
            time_samples.append(now - last_time)
        last_time = now

    if counter == sample_count:
        print()

        if write:
            export_calibration_data()

        average_time = sum(time_samples) / len(time_samples)
        print(f"SPS: {1 / average_time:.2f}")

        sys.exit(0)
              
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-w", "--write", action="store_true")
    args = parser.parse_args()

    sensors = HWSensors(lambda coords, value: on_sensor_reading(coords, value, args.write))

    print()
    asyncio.run(sensors.sensor_reading_loop())
