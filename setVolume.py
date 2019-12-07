import json, config
from filelock import Timeout, FileLock


def main():
    with open(config.datafile) as json_file:
        data = json.load(json_file)

    data['volume'] = 90

    lock = FileLock(config.datafile_lock)
    with lock:
        raw_json  = json.dumps(data)
        open(config.datafile, "w").write(raw_json)


if __name__ == "__main__":
    main()

