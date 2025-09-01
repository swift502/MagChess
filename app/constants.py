import json
from utilities import data_path

# Flags
DEV_LAYOUT = False
RPI = True
ENGINE = True

# Sensors
with open(data_path("sensor_calibration_data.json")) as f:
    SENSOR_CALIBRATION_DATA: dict[str, int] = json.load(f)
SENSOR_TRIGGER_DELTA = 500
SENSOR_SIM_NOISE = 100

# Themes
# Green
THEME_WHITE = "#eeeed5"
THEME_BLACK = "#7d945d"

# Brown
# THEME_WHITE = "#f0d9b5"
# THEME_BLACK = "#b58863"