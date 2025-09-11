#!/bin/bash

sudo apt update
sudo apt install mpv libmpv2 libmpv-dev

sudo grep -q '^dtoverlay=i2c1,pins_2_3,baudrate=' /boot/firmware/config.txt \
  && sudo sed -i 's/^dtoverlay=i2c1,pins_2_3,baudrate=.*/dtoverlay=i2c1,pins_2_3,baudrate=400000/' /boot/firmware/config.txt \
  || echo 'dtoverlay=i2c1,pins_2_3,baudrate=400000' | sudo tee -a /boot/firmware/config.txt

arch=$(dpkg-architecture -qDEB_HOST_MULTIARCH)
mkdir -p ~/.local/lib
ln -s /usr/lib/$arch/libmpv.so.2 ~/.local/lib/libmpv.so.1

if [ ! -d ".venv" ]; then
    python -m venv .venv
source ".venv/bin/activate"
pip install -r requirements.txt
deactivate
