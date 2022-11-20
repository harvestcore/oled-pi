# SH1106 OLED screen setup for RPI

## Base install

```bash
sudo apt-get update
sudo apt-get upgrade
sudo reboot

sudo apt install python3-pip
sudo pip3 install --upgrade setuptools
```

## Install the Luma libraries

```bash
pip3 install luma-core
pip3 install luma-oled
```

## GPIO Connection

- GND / GND / GPIO 9
- VDD / VCC / GPIO 1
- SCK / SCL / GPIO 5
- SDA / SDA / GPIO 3

## Check the `I2C` status

```bash
sudo i2cdetect -y 1

    0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
00:                         -- -- -- -- -- -- -- --
10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
30: -- -- -- -- -- -- -- -- -- -- -- -- 3c -- -- --
40: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
60: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
70: -- -- -- -- -- -- -- --
```

## Run the script

```bash
python3 stats.py
```

## Run on boot

```bash
crontab -e

# Add this line to the end of the file.
@reboot python3 /path/to/stats.py &
```

## Icons

[Line Awesome](https://icons8.com/line-awesome)
