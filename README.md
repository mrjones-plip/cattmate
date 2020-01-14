# Cattmate

A WiFi enabled physical volume knob for Chromecasts via a mash up of Griffin's no longer made USB device the 
[PowerMate](https://support.griffintechnology.com/product/powermate/) and
the awesome python Chromecast controlling library [catt](https://github.com/skorokithakis/catt/)
using the equally awesome [powermate](https://github.com/bethebunny/powermate)
 python library. You can optionally show the volume on a screen.

Here's the current demo in an animated gif.  Behind the PowerMate is a Chromebook running the
Google Home app.  When the Cattmate sets the volume you 
can kinda make out Google Home reflect the volume change as well:

![](./demo4.gif)

## Status   

This is my first real Python project!  That means while the code is super stable 
(my desktop version has an uptime of weeks now), I'm guessing not everything follows the
[Pythonic way](https://docs.python-guide.org/writing/style/) just so.


## Hardware

* Raspbery Pi - I used a [Raspberry Pi Model 3B Rev 1.2](https://amzn.to/2REZXwb)
* [PowerMate](https://support.griffintechnology.com/product/powermate/) - Hopefully you 
can [find one used on eBay](https://www.ebay.com/sch/i.html?_nkw=griffin+powermate+usb+-bluetooth) if 
you don't already have one
* 0.96" SSD1336 OLED Screen (_optional_) - I use [these from MakerFocus](https://amzn.to/2PKMQqL)
* [Chromecast](https://en.wikipedia.org/wiki/Chromecast) - any sort will do, original, audio or ultra

## Use

Cattmate supports:

* Increase volume - rotate clockwise
* Decrease volume - rotate counter-clockwise
* Mute - push down - the light will strobe to denote muted status
* Unmute - push down again
* Pause - push down and hold 1+ second
* Play - push down and hold 1+ second again
* Fast Forward - push down and rotate clockwise
* Rewind - push down and rotate counter-clockwise

## Install

These steps assume you have your Pi set up with Raspbian, that it's booted up, connected
to the same WiFi as your Chromecast. If your Chromecast is on a different network, but 
you can get to it by IP, the
config supports IPs instead of Chromecast names.  It also assumes you're using the `pi`
default user with a home directory of `/home/pi` and that you have both 
[pip3](https://pip.pypa.io/en/stable/installing/) and optionally 
[virtualenv](https://virtualenv.pypa.io/en/stable/) installed:

1. Clone this repo and cd into it:
 `git clone https://github.com/Ths2-9Y-LqJt6/cattmate.git /home/pi/cattmate; cd /home/pi/cattmate`
1. Create your own virtualenv and activate it `python3 -m venv venv;. venv/bin/activate` (_optional_)
1. Install all the python prerequisites with `pip3 install -r requirements.txt`
1. Create your own config file `cp config.dist.py config.dist` and edit `config.dist` with 
the names or IPs
of the chromecasts you want to use (ony first one supported right now ;) and whether you want
to use an external I2C screen or not
1. Copy the systemd file into place, reload systemd, start and enable it:
    ```bash
    sudo cp cattmate.service /etc/systemd/system/
    sudo systemctl daemon-reload
    sudo systemctl enable cattmate
    sudo systemctl start cattmate
    ```
1. Add the ``udev`` rule with ``sudo cp 60-powermate.rules /etc/udev/rules.d/`` and plug your 
powermate into an open USB port.  

You should be good to go!  The system is very resilient in that you can not have screen plugged
in when you start and the plug it in and systemd will notice and start things up.  Same 
for the powermatte - you can unplug and plug and unplug all day and it satisfyingly just works!

# Troubleshooting 

You can debug the system in syslog with `sudo tail -f /var/log/syslog`. I try to do a lot 
of testing and explicit have `except` errors that expictly tell you what went wrong
and how to fix it.  If all else fails, open an issue and I'l try and help ya!


## Releases

* 14 Jan 2020 v0.5 - Rewrite readme, add both `cattmate.service` and `60-powermate.rules` for
systemd and udev rules respectively. 
* 16 Dec 2019 v0.13 - Complete refactor to use native python driver
per [#8](https://github.com/Ths2-9Y-LqJt6/cattmate/issues/8) and add pause, ff & rrwnd per
  [#10](https://github.com/Ths2-9Y-LqJt6/cattmate/issues/10)
* 13 Dec 2019 v0.12 - Add MIN/MAX alerts per [#2](https://github.com/Ths2-9Y-LqJt6/cattmate/issues/2), fix 
[#1](https://github.com/Ths2-9Y-LqJt6/cattmate/issues/1)
* 10 Dec 2019 v0.11 - refactor `ssd1306` lib  to `Csd1306` class, simplify calls to same, refactor for cleaner code 
* 10 Dec 2019 v0.10 - first decently functional code, known issue 
in [#1](https://github.com/Ths2-9Y-LqJt6/cattmate/issues/1) though.
