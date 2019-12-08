import time, json, os.path, config
from filelock import Timeout, FileLock


def create_volume_file():
    lock = FileLock(config.volumefile_lock, timeout=1)
    with lock:
        open(config.volumefile, "w").write('10')


def main():
    if not os.path.isfile(config.volumefile):
        create_volume_file()

    try:
        lock = FileLock(config.volumefile_lock, timeout=1)
        with lock:
            volume = open(config.volumefile, "r").read()
    except TypeError:
        create_volume_file()
        volume = '10'

    current_volume = volume

    print('start: ' + current_volume)

    while True:
        lock = FileLock(config.volumefile_lock, timeout=1)
        with lock:
            volume = open(config.volumefile, "r").read()

        if volume != current_volume:
            current_volume = volume
            print('update: ' + volume)

        time.sleep(config.refresh_wait)


if __name__ == "__main__":
    main()