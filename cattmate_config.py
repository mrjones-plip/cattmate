
# this unused for now
prototypical_data = {}
prototypical_data['volume'] = 10
prototypical_data['album'] = None
prototypical_data['artist'] = None
prototypical_data['thumb'] = None

# this unused for now
datafile = './cattmate.json'
datafile_lock = './.cattmate.json.lock'

# volume file is a single line with int from -1 = 101
volumefile = './volume.txt'
volumefile_lock = './.volume.txt.lock'

# how often to wait at the end of the master 'while True;' loop
# controls how often the screen is updated
refresh_wait = 0.01
