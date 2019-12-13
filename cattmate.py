import time, cattmate_config, config, socket, sys, logging
from Oled import Oled
from os import system
import catt.api as cat_api
from filelock import FileLock


def get_volume_from_file():
    lock = FileLock(cattmate_config.volumefile_lock, timeout=1)
    with lock:
        volume = open(cattmate_config.volumefile, "r").read().strip()
    return volume


def create_volume_file():
    lock = FileLock(cattmate_config.volumefile_lock, timeout=1)
    with lock:
        open(cattmate_config.volumefile, "w").write(cattmate_config.prototypical_data['volume'])


# thanks https://stackoverflow.com/a/5998359
def milli_time():
    return int(round(time.time() * 1000))


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


def main():

    if config.use_display:
        print('Trying to initialize screen on bus /dev/i2c-' + str(config.display_bus))
        try:
            screen = Oled(config.display_bus, config.font_size)
        except FileNotFoundError as e:
            exit('ERROR Could not access screen. Wrong I2C buss specified? Using /dev/i2c-' + str(config.display_bus))
        except Exception as e:
            # todo - where does this logging go? what other errors could end up here?
            logging.exception(e)
            exit('ERROR Could not access screen: ' + str(e))
    
    # make sure we have a good file and volume
    try:
        volume = get_volume_from_file()
    except TypeError:
        create_volume_file()
        volume = cattmate_config.prototypical_data['volume']

    # remember current volume and let user know we're starting
    current_volume = volume
    last_volume_update = milli_time()
    need_update = False
    print('Trying to start with: ' + str(config.chromecasts[0]))

    try:
        cast = get_cast_handle(config.chromecasts[0])
    except cat_api.CastError:
        sys.exit("ERROR: Couldn't connect to '" + config.chromecasts[0] + "'. Check config.py and name/IP.")

    if config.use_display:
        screen.display(current_volume)

    print(current_volume)

    # enter endless loop to check file for volume updates
    while True:

        # get the volume from the file at the top of the loop
        volume = get_volume_from_file()

        # if the volume has changed and it's not empty, update chromecast and screen
        if volume != current_volume and volume:
            current_volume = volume
            last_volume_update = milli_time()
            need_update = True
            if config.use_display:
                screen.display(current_volume)
            _ = system('clear')
            print(volume)

        # wait 400ms since last local volume change before sending update to chromecast
        if need_update & (milli_time() - last_volume_update > 400):
            need_update = False
            cast.volume(int(volume)/100)
            print('send vol update: ' + str(current_volume))

            if config.use_display:
                time.sleep(cattmate_config.refresh_wait)
                screen.display(current_volume + ' ;)')
                time.sleep(cattmate_config.refresh_wait)
                screen.display(current_volume)

        # wait a certain amount of time so we don't over load the system with file reads
        time.sleep(cattmate_config.refresh_wait)


if __name__ == "__main__":
    main()
