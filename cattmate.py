import time, cattmate_config, config
from catt.api import CattDevice
from filelock import FileLock


def get_volume_from_file():
    lock = FileLock(cattmate_config.volumefile_lock, timeout=1)
    with lock:
        volume = open(cattmate_config.volumefile, "r").read().strip()
    return volume


def create_volume_file():
    lock = FileLock(cattmate_config.volumefile_lock, timeout=1)
    with lock:
        open(cattmate_config.volumefile, "w").write('10')


# thanks https://stackoverflow.com/a/5998359
def milli_time():
    return int(round(time.time() * 1000))


def main():
    # make sure we have a good file and volume
    try:
        volume = get_volume_from_file()
    except TypeError:
        create_volume_file()
        volume = '10'

    # remember current volume and let use know we're starting
    current_volume = volume
    last_volume_update = milli_time()
    need_update = False
    print('Trying to start with: ' + str(config.chromecasts[0]))

    cast = CattDevice(name=config.chromecasts[0])

    print('start: ' + current_volume)

    # enter endless loop to check file for volume updates
    while True:
        volume = get_volume_from_file()
        # todo - some times I see a "update: ", as if the new volume was empty? Error check somehwere...
        if volume != current_volume:
            current_volume = volume
            last_volume_update = milli_time()
            need_update = True
            print('update: ' + volume)

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
