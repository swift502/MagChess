import json
from utilities import data_path

# Flags
DEV_LAYOUT = False
RPI = False
ENGINE = True

# Sensors
with open(data_path("sensor_calibration_data.json")) as f:
    SENSOR_CALIBRATION_DATA = json.load(f)
SENSOR_TRIGGER_DELTA = 500

# Themes
# Green
THEME_WHITE = "#eeeed5"
THEME_BLACK = "#7d945d"

# Brown
# THEME_WHITE = "#f0d9b5"
# THEME_BLACK = "#b58863"