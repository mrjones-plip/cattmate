# Castmate

A WiFi enabled physical volume knob for Chromecasts via a mash up of Griffin's no longer made USB device the 
[PowerMate](https://support.griffintechnology.com/product/powermate/) and
the awesome python Chromecast controlling library [catt](https://github.com/skorokithakis/catt/)
using the equally awesome [powermate-linux](https://github.com/stefansundin/powermate-linux)
 app.

**Note** - This project is very much a work in progress. It is not fully functional yet! Don't 
use unless you're looking to learn and experiement like am right now ;)   

## Install

1. Make sure the following requirements are installed:
   * [powermatte-linux](https://github.com/stefansundin/powermate-linux)
   * [pip](https://pip.pypa.io/en/stable/installing/)
   * [virtualenv](https://virtualenv.pypa.io/en/stable/) 
1. Clone this repo `git clone https://github.com/Ths2-9Y-LqJt6/cattmate.git`
1. Change directories to cattmate `cd cattmate`
1. Create your own virtualenv and activate it `python3 -m venv venv;. venv/bin/activate` (_optional_)
1. Install all the python prerequesites with `pip install -r requirements.txt`
1. Edit `powermate.toml` with the paths to python3 and powermate binary for the four
`*_command` commands
1. Start the cattmate controller `python3 cattmate.py` and start the powermatte-linux software
specifying the config file you edited above: `/usr/bin/powermate -c powermate.toml`
