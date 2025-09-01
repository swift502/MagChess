# MagChess

Magnetic chess game detection for the [Traditional Chess Lego Set](https://www.lego.com/en-cz/product/traditional-chess-set-40719), ADS1015 and Raspberry Pi.

## Run notes

1. Run rpi_install.sh
2. Insert `dtoverlay=i2c1,pins_2_3,baudrate=400000` into `/boot/firmware/config.txt`
3. Reboot
4. Run rpi_run.sh