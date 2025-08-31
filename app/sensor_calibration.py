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
    path = data_path("sensor_calibration_data.json")
    with open(path, "w") as f:
        json.dump(average, f, indent=4)

    average_time = sum(time_samples) / len(time_samples)

    print(f'\nWritten "{path}"')
    print(f"SPS: {1 / average_time:.2f}")

def on_sensor_reading(values: SensorReading):
        samples.append(values)
        print(f"\rSampled {len(samples)}/{sample_count}", end="")

        global time_samples, last_time
        now = time.perf_counter()
        if last_time is not None:
            time_samples.append(now - last_time)
        last_time = now

        if len(samples) == sample_count:
             export_calibration_data()
             sys.exit(0)
              
if __name__ == "__main__":
    sensors = HWSensors(on_sensor_reading)

    print()
    asyncio.run(sensors.sensor_reading_loop())
