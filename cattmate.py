import time, config
from filelock import FileLock


def get_volume_from_file():
    lock = FileLock(config.volumefile_lock, timeout=1)
    with lock:
        volume = open(config.volumefile, "r").read()
    return volume


def create_volume_file():
    lock = FileLock(config.volumefile_lock, timeout=1)
    with lock:
        open(config.volumefile, "w").write('10')


def main():

    # make sure we have a good file and volume
    try:
        volume = get_volume_from_file()
    except TypeError:
        create_volume_file()
        volume = '10'

    # remember current volume and let use know we're starting
    current_volume = volume
    print('start: ' + current_volume)

    # enter endless loop to check file for volume updates
    while True:
        volume = get_volume_from_file()
        if volume != current_volume:
            current_volume = volume
            print('update: ' + volume)

        # wait a certain amount of time so we don't over load the system with file reads
        time.sleep(config.refresh_wait)

if __name__ == "__main__":
    main()