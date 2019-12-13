#!/usr/bin/python
import Adafruit_SSD1306
import os
from os import system
from PIL import Image, ImageDraw, ImageFont


class Oled:

    def __init__(self, display_bus, font_size):
        # declare member variables
        self.draw = None
        self.font = None
        self.disp = None
        self.width = None
        self.height = None
        self.image = None
        self.font_size = font_size

        # display bus
        # Rev 2 Pi, Pi 2 & Pi 3 uses bus 1
        # Rev 1 Pi uses bus 0
        # Orange Pi Zero uses bus 0 for pins 1-5 (other pins for bus 1 & 2)
        self.display_bus = display_bus

        # init
        self.initialize()

    def initialize(self):
        # 128x64 display with hardware I2C:
        self.disp = Adafruit_SSD1306.SSD1306_128_64(rst=None, i2c_bus=self.display_bus)

        # Initialize library.
        self.disp.begin()

        # Clear display.
        self.disp.clear()
        self.disp.display()

        # Create blank image for drawing.
        # Make sure to create image with mode '1' for 1-bit color.
        self.width = self.disp.width
        self.height = self.disp.height
        self.image = Image.new('1', (self.width, self.height))

        # Get drawing object to draw on image.
        self.draw = ImageDraw.Draw(self.image)

        # set full puth for incling libs below
        full_path = os.path.dirname(os.path.abspath(__file__)) + "/"

        # Draw a black filled box to clear the image.
        self.draw.rectangle((-20, -20, self.width, self.height), outline=0, fill=0)
        self.font = ImageFont.truetype(full_path + "Lato-Heavy.ttf", self.font_size)

    def display(self, text):
        # Draw some shapes.
        # First define some constants to allow easy resizing of shapes.
        padding = -2
        top = padding
        # bottom = self.height - padding

        # Draw a black filled box to clear the image.
        self.draw.rectangle((0, 0, self.width, self.height), outline=0, fill=0)
        self.draw.text((0, top + 10), str(text), font=self.font, fill=255)

        # Display image.
        self.disp.image(self.image)
        self.disp.display()
