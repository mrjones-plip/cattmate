import time, cattmate_config, config, socket, sys
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
    # make sure we have a good file and volume
    try:
        volume = get_volume_from_file()
    except TypeError:
        create_volume_file()
        volume = cattmate_config.prototypical_data['volume']

    # remember current volume and let use know we're starting
    current_volume = volume
    last_volume_update = milli_time()
    need_update = False

    # todo - check for IPv6 too socket.inet_pton(socket.AF_INET6, some_string)
    print('Trying to start with: ' + str(config.chromecasts[0]))
    try:
        cast = get_cast_handle(config.chromecasts[0])
    except cat_api.CastError:
        sys.exit("ERROR: Could not connect to '" + config.chromecasts[0] + "'. Check config.py and name/IP and try again.")

    _ = system('clear')
    print(current_volume)

    # enter endless loop to check file for volume updates
    while True:
        volume = get_volume_from_file()
        if volume != current_volume and volume:
            current_volume = volume
            last_volume_update = milli_time()
            need_update = True
            _ = system('clear')
            print(volume)

        # wait 400ms since last local volume change before sending update to chromecast
        if need_update & (milli_time() - last_volume_update > 400):
            need_update = False
            cast_volume = int(volume)/100;
            cast.volume(cast_volume)
            print('send vol update: ' + str(cast_volume))

        # wait a certain amount of time so we don't over load the system with file reads
        time.sleep(cattmate_config.refresh_wait)


if __name__ == "__main__":
    main()
