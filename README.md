# MagChess

Magnetic chess game detection for the [Traditional Chess Lego Set](https://www.lego.com/en-cz/product/traditional-chess-set-40719), ADS1015 and Raspberry Pi.

## Run notes

1. Run rpi_install.sh
2. Run rpi_run.sh

## Autostart

```bash
mkdir -p ~/.config/autostart
nano ~/.config/autostart/magchess.desktop
```

```ini
[Desktop Entry]
Type=Application
Name=MagChess
Exec=/home/pi/Documents/Github/MagChess/rpi_run.sh
```
