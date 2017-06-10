import gzip
import json
import platform
import pickle

def get_artist_counts(artfile):
    painting_metadata = json.load(artfile)
    artist_counts = {}
    for data in painting_metadata:
        artists = data['artist']
        if len(artists) == 0:
            continue
        artist = artists[0]
        if artist in artist_counts:
            artist_counts[artist] += 1
        else:
            artist_counts[artist] = 1
    return artist_counts
  
def load_pickle(f):
    buf = ''
    while True:
        data = f.read()
        if data == "":
            break
        buf += data
    o = pickle.loads(buf)
    f.close()
    return o
    
    
threshold = 25

def filter_uncommon(images, ids, artist_counts):
    indices_to_keep = []
    nimages = len(ids)
    for i in xrange(nimages):
        count = artist_counts[ids[i]]
        if count >= threshold:
            indices_to_keep.append(i)
    good_images = [images[i] for i in indices_to_keep]
    good_ids = [ids[i] for i in indices_to_keep]
    return good_images, good_ids


'''
pickle_and_next_batch

Saves current datadict to a .pkl (scheme is data/data_batch_<currBatch>.pkl)
'''
def pickle_and_next_batch(datadict, outfilename):
	f = gzip.GzipFile(outfilename, 'wb')
	pickle.dump(datadict, f)
	f.close()


artfile = open('downsized_art.json', 'r')
artist_counts = get_artist_counts(artfile)
'''
count = 0
for artist in artist_counts:
    if artist_counts[artist] >= threshold:
        count += 1
print ('There are ' + str(count) + ' artists')
'''

for i in range(9):
    filename = 'data/data_batch_' + str(i) + '.pgz'
    outfilename = 'filtered_data/data_batch_' + str(i) + '.pgz'
    with gzip.open(filename, 'rb') as pickle_file:
        datadict = load_pickle(pickle_file)
        X = datadict['data']
        Y = datadict['labels']
        
        X, Y = filter_uncommon(X, Y, artist_counts)
        for obj_id in Y:
            if artist_counts[obj_id.strip()] < threshold:
                print ('bad')
                
        #pickle_and_next_batch({'data': X, 'labels': Y}, outfilename)
        
        