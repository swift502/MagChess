import json
import platform
from utilities import root_path

# Flags
DEV_LAYOUT = False
RPI = platform.machine() == "aarch64"

# Sensors
with open(root_path("calibration_data.json")) as f:
    SENSOR_CALIBRATION_DATA: dict[str, int] = json.load(f)
SENSOR_TRIGGER_DELTA = 500
SENSOR_SIM_NOISE = 100

# Themes
THEME_WHITE = "#eeeed5"
THEME_BLACK = "#7d945d"
