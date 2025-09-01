import argparse
import asyncio
import json
import sys
import time

from data import SensorReading
from sensors_hw import HWSensors
from utilities import data_path

sample_count = 10
samples: list[SensorReading] = []

time_samples: list[float] = []
last_time: float | None = None

def export_calibration_data():
    average = {str(coords): sum(sample[coords] for sample in samples) // len(samples) for coords in samples[0]}
    average = dict(sorted(average.items()))
    path = data_path("sensor_calibration_data.json")
    with open(path, "w") as f:
        json.dump(average, f, indent=4)

    print(f'\nWritten "{path}"')

def on_sensor_reading(values: SensorReading, write: bool):
    samples.append(values)
    print(f"\rSampled {len(samples)}/{sample_count}", end="")

    global time_samples, last_time
    now = time.perf_counter()
    if last_time is not None:
        time_samples.append(now - last_time)
    last_time = now

    if len(samples) == sample_count:
        if write:
            export_calibration_data()

        average_time = sum(time_samples) / len(time_samples)
        print(f"SPS: {1 / average_time:.2f}")

        sys.exit(0)
              
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-w", "--write", action="store_true", help="Write calibration data to file")
    args = parser.parse_args()

    # Pass write argument to HWSensors
    sensors = HWSensors(lambda values: on_sensor_reading(values, write=args.write))

    print()
    asyncio.run(sensors.sensor_reading_loop())
