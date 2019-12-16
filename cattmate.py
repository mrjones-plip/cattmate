import time, cattmate_config, config, socket, sys, logging, os, glob
from powermate.powermate import PowerMateBase, LedEvent
from Oled import Oled
import catt.api as cat_api


# thanks https://stackoverflow.com/a/5998359
def milli_time():
    return int(round(time.time() * 1000))


MAX_VOLUME = 100


def get_cast_handle(name_or_ip):
    try:
        socket.inet_pton(socket.AF_INET6, config.chromecasts[0])
        cast = cat_api.CattDevice(ip_addr=config.chromecasts[0])
    except socket.error:
        try:
            socket.inet_aton(config.chromecasts[0])
            cast = cat_api.CattDevice(ip_addr=config.chromecasts[0])
        except socket.error:
            cast = cat_api.CattDevice(name=config.chromecasts[0])
    return cast


class cattmate(PowerMateBase):
    def __init__(self, path):

        logging.basicConfig(filename=os.path.dirname(os.path.abspath(__file__)) + "/error.log")
        print('Initializing PowerMate: ' + path)

        try:
            glob_path = glob.glob(path)[0]
            super(cattmate, self).__init__(glob_path)
        except IndexError as e:
            logging.error(logging.exception(e))
            sys.exit("ERROR: Couldn't connect PowerMate at '" + path +
                     "'. Is it plugged in and is the udev file installed per readme.md?")
        self._pulsing = False
        self._volume = 20

        print('Trying to get handle to Chromecast: ' + config.chromecasts[0])
        try:
            self.cast = get_cast_handle(config.chromecasts[0])
        except cat_api.CastError as e:
            logging.error(logging.exception(e))
            sys.exit("ERROR: Couldn't connect to '" + config.chromecasts[0] + "'. Check config.py and name/IP.")

        if config.use_display:
            print('Trying to initialize screen on bus /dev/i2c-' + str(config.display_bus))
            try:
                self.screen = Oled(config.display_bus, config.font_size)
            except FileNotFoundError as e:
                exit('ERROR Could not access screen. Wrong I2C buss in "config.display_bus"? ' + "\n" +
                     'Using /dev/i2c-' + str(config.display_bus) + "\n" +
                     'Error: ' + str(e)
                     )
            except Exception as e:
                logging.error(logging.exception(e))
                exit('ERROR Could not access screen: ' + str(e))
        else:
            self.screen = False

        print('Successfully started!')

    def short_press(self):
        self._pulsing = not self._pulsing
        if self._pulsing:
            print('Muted')
            self.cast.volume(0)

            if config.use_display:
                try:
                    self.screen.display('MUTE')
                except Exception as e:
                    logging.error(logging.exception(e))
            return LedEvent.pulse()
        else:
            if config.use_display:
                try:
                    self.screen.display(str(self._volume))
                except Exception as e:
                    logging.error(logging.exception(e))
            print('Unmuted')
            self.cast.volume(int(self._volume) / 100)
            return LedEvent(brightness=self._volume)

    def long_press(self):
        print('Pause?')

    def rotate(self, rotation):
        self._volume = max(0, min(MAX_VOLUME, self._volume + rotation))
        self._pulsing = False

        if config.use_display:
            try:
                self.screen.display(str(self._volume))
            except Exception as e:
                logging.error(logging.exception(e))

        self.cast.volume(int(self._volume) / 100)
        print('send vol update: ' + str(self._volume))

        return LedEvent(brightness=self._volume)

    def push_rotate(self, rotation):
        print('Push rotate {}!'.format(rotation))


if __name__ == "__main__":
    print("Trying to start...")
    pm = cattmate('/dev/input/by-id/*PowerMate*')
    pm.run()
