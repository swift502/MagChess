import asyncio
import json
import sys

from data import SensorReading
from sensors_hw import HWSensors
from utilities import data_path

sample_count = 10
samples: list[SensorReading] = []

def export_calibration_data():
    average = {str(coords): sum(sample[coords] for sample in samples) // len(samples) for coords in samples[0]}

    path = data_path("sensor_calibration_data.json")
    with open(path, "w") as f:
        json.dump(average, f, indent=4)

    print(f'Written "{path}"')

def on_sensor_reading(values: SensorReading):
        samples.append(values)
        print(f"Sampled {len(samples)}/{sample_count}", end="\r")

        if len(samples) == sample_count:
             export_calibration_data()
             sys.exit(0)
              
if __name__ == "__main__":
    sensors = HWSensors(on_sensor_reading)
    asyncio.run(sensors.sensor_reading_loop())