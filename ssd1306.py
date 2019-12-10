#!/usr/bin/python
import config
import os
import Adafruit_SSD1306
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

# set full puth for including libs below
full_path = os.path.dirname(os.path.abspath(__file__)) + "/"

# Raspberry Pi pin configuration:
RST = None     # on the PiOLED this pin isnt used
# Note the following are only used with SPI:
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0


# todo - this is an awkward architecture...move to class?
def get_display_handle():
    # 128x64 display with hardware I2C:
    return Adafruit_SSD1306.SSD1306_128_64(rst=RST, i2c_bus=config.display_bus)


def display(display, text, size, clear=False):
    # Initialize library.
    display.begin()

    # Clear display.
    if clear:
        display.clear()
        display.display()


    # Create blank image for drawing.
    # Make sure to create image with mode '1' for 1-bit color.
    width = display.width
    height = display.height
    image = Image.new('1', (width, height))

    # Get drawing object to draw on image.
    draw = ImageDraw.Draw(image)

    # Draw a black filled box to clear the image.
    draw.rectangle((-20, -20, width, height), outline=0, fill=0)

    # Draw some shapes.
    # First define some constants to allow easy resizing of shapes.
    padding = -2
    top = padding
    bottom = height - padding
    font = ImageFont.truetype(full_path + "Lato-Heavy.ttf", size)

    # Draw a black filled box to clear the image.
    draw.rectangle((0,0,width,height), outline=0, fill=0)
    draw.text((0, top), text , font=font, fill=255)
    # Display image.
    display.image(image)
    display.display()
