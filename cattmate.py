import time, json, os.path, config
from filelock import Timeout, FileLock


def get_default_json():
    return config.prototypical_data


def create_data_file():
    data = get_default_json()
    lock = FileLock(config.datafile_lock)
    with lock:
        raw_json  = json.dumps(data);
        open(config.datafile, "w").write(raw_json)


def main():
    if not os.path.isfile(config.datafile):
        create_data_file()

    try:
        lock = FileLock(config.datafile_lock)
        with lock:
            raw_json = open(config.datafile, "r")
            data = json.load(raw_json)
    except TypeError:
        create_data_file()
        data = config.prototypical_data

    current_volume = data['volume']

    print('start: ' + str(current_volume))

    while True:
        lock = FileLock(config.datafile_lock)
        with lock:
            raw_json = open(config.datafile, "r")
            data = json.load(raw_json)

        if data['volume'] != current_volume:
            current_volume = data['volume']
            print('update: ' + str(current_volume))

        time.sleep(config.refresh_wait)


if __name__ == "__main__":
    main()