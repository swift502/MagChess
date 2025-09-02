# MagChess

![](images/preview.png)

Magnetic chess game interpreter and recorder for the Lego [Traditional Chess Set](https://www.lego.com/en-cz/product/traditional-chess-set-40719). Game PGN can be copied to clipboard or uploaded as a Gist via Github CLI. 

## App

Setup

```bash
pip install -r requirements.txt
rpi_install.sh
```

Run

```bash
rpi_run.sh
```

### Autostart config

```bash
mkdir -p ~/.config/autostart
nano ~/.config/autostart/magchess.desktop
```

```ini
[Desktop Entry]
Type=Application
Name=MagChess
Icon=/home/pi/Documents/Github/MagChess/app/assets/icon.ico
Exec=/home/pi/Documents/Github/MagChess/rpi_run.sh
```

## Used components

- Raspberry Pi 5
- Waveshare 4inch HDMI LCD (C)
- 64x SS49E hall sensor
- 4x CD74HC4067 (mux)
- ADS1015 (adc)
- MP1584EN (step down)
- Pin headers, wires
