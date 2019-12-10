#!/usr/bin/python
import os
import Adafruit_SSD1306
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont


class Ssd1306:

    def __init__(self, display_bus, font_size):
        # 128x64 display with hardware I2C:
        self.screen = Adafruit_SSD1306.SSD1306_128_64(rst=None, i2c_bus=display_bus)
        self.font_size = font_size

    def display(self, text, clear=False):
        # Initialize library.
        self.screen.begin()

        # Clear display.
        if clear:
            self.screen.clear()
            self.screen.display()

        # Create blank image for drawing.
        # Make sure to create image with mode '1' for 1-bit color.
        width = self.screen.width
        height = self.screen.height
        image = Image.new('1', (width, height))

        # Get drawing object to draw on image.
        draw = ImageDraw.Draw(image)

        # Draw a black filled box to clear the image.
        draw.rectangle((-20, -20, width, height), outline=0, fill=0)

        # Draw some shapes.
        # First define some constants to allow easy resizing of shapes.
        padding = -2
        top = padding
        font = ImageFont.truetype(
            os.path.dirname(os.path.abspath(__file__)) + "/" + "Lato-Heavy.ttf",
            self.font_size
        )

        # Draw a black filled box to clear the image.
        draw.rectangle((0, 0, width, height), outline=0, fill=0)
        draw.text((0, top), str(text), font=font, fill=255)
        # Display image.
        self.screen.image(image)
        self.screen.display()