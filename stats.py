import subprocess
from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import sh1106
from gpiozero import Button
from signal import pause
from PIL import ImageFont
from threading import Thread
from time import sleep

LOOPTIME = 1

# Button on GPIO 23.
button = Button(23)

# Font
font = ImageFont.truetype('/home/pi/OLED_Stats/PixelOperator.ttf', 16)
icon_font= ImageFont.truetype('/home/pi/OLED_Stats/lineawesome-webfont.ttf', 18)

# SH1106 device.
device = sh1106(i2c(port=1, address=0x3C), width=128, height=64, rotate=0)
device.clear()

stop_threads = False
hide_stats = False
thread = None

def clear():
	global device
	device.clear()

def stats():
	global device
	global stop_threads
	while(True and not stop_threads):
		with canvas(device) as draw:
			cmd = "hostname -I | cut -d\' \' -f1 | head --bytes -1"
			IP = subprocess.check_output(cmd, shell = True )

			cmd = "top -bn1 | grep load | awk '{printf \"%.2fLA\", $(NF-2)}'"
			CPU = subprocess.check_output(cmd, shell = True )

			cmd = "free -m | awk 'NR==2{printf \"%.2f%%\", $3*100/$2 }'"
			MemUsage = subprocess.check_output(cmd, shell = True )

			cmd = "df -h | awk '$NF==\"/\"{printf \"%d/%dGB\", $3,$2}'"
			Disk = subprocess.check_output(cmd, shell = True )

			cmd = "vcgencmd measure_temp | cut -d '=' -f 2 | head --bytes -1"
			Temperature = subprocess.check_output(cmd, shell = True )

			draw.text((0, 5),  chr(63339),  font=icon_font, fill=255) # Icon temp
			draw.text((64, 5), chr(62776),  font=icon_font, fill=255) # Icon memory
			draw.text((0, 25), chr(63426),  font=icon_font, fill=255) # Icon disk
			draw.text((64, 25), chr(62171), font=icon_font, fill=255) # Icon cpu
			draw.text((0, 45), chr(61931),  font=icon_font, fill=255) # Icon wifi
			
			draw.text((19, 5), str(Temperature,'utf-8'),  font=font, fill=255) # Text temperature
			draw.text((87, 5), str(MemUsage,'utf-8'),  font=font, fill=255) # Text memory usage
			draw.text((19, 25), str(Disk,'utf-8'),  font=font, fill=255) # Text Disk usage
			draw.text((87, 25), str(CPU,'utf-8'), font=font, fill=255) # Text cpu usage

			if len(IP) == 0:
				draw.text((35, 45), chr(61721),  font=icon_font, fill=255) # No IP icon
			else:
				draw.text((19, 45), str(IP,'utf-8'),  font=font, fill=255) # Text IP address

			draw.text((105, 45), chr(63035),  font=icon_font, fill=255) # Extra icon

		sleep(LOOPTIME)

def toggle_stats():
	global hide_stats
	global stop_threads
	global thread

	if hide_stats:
		clear()
		stop_threads = True
		if thread is not None:
			thread.join()
	else:
		stop_threads = False
		thread = Thread(target=stats)
		thread.start()

	hide_stats = not hide_stats

button.when_pressed = toggle_stats

pause()
