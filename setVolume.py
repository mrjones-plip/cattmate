import json, argparse, config
from filelock import FileLock

parser = argparse.ArgumentParser()
parser.add_argument('--volume', '-v', type=str, help='Pass "up", "down", "zero" or int of specific volume')
args = parser.parse_args()


# thanks https://stackoverflow.com/a/1267145
def RepresentsInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


def main():
    with open(config.datafile) as json_file:
        data = json.load(json_file)

    if args.volume == 'up' and data['volume'] < 100:
        data['volume'] = data['volume'] + 1

    elif args.volume == 'down' and data['volume'] > 0:
        data['volume'] = data['volume'] - 1

    elif args.volume == 'zero':
        data['volume'] = 0

    elif RepresentsInt(args.volume) and 100 > args.volume > 0:
        data['volume'] = int(args.volume)

    lock = FileLock(config.datafile_lock)
    with lock:
        raw_json = json.dumps(data)
        open(config.datafile, "w").write(raw_json)


if __name__ == "__main__":
    main()

