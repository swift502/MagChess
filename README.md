# MagChess

![](images/preview.png)

Magnetic chess game interpreter and recorder for the Lego [Traditional Chess Set](https://www.lego.com/en-cz/product/traditional-chess-set-40719), Raspberry Pi, ADS1015 and SS49E magnetic sensors.

- Copy game PGN to clipboard
- Upload game PGN as a Github Gist

## Run

1. Run `rpi_install.sh`
2. Run `rpi_run.sh`

## Autostart

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
