import json

def get_artist_counts(artfile):
    painting_metadata = json.load(artfile)
    artist_counts = {}
    artist_to_ids = {}
    metadata_index = {}
    for data in painting_metadata:
        artists = data['artist']
        if len(artists) == 0:
            continue
        artist = artists[0]
        # painting_to_artist[data['id']] = artist
        metadata_index[data['id']] = {'description': data['description'], 'artist': artist}
        
        if artist in artist_counts:
            artist_counts[artist] += 1
            artist_to_ids[artist].append(data['id'])
        else:
            artist_counts[artist] = 1
            artist_to_ids[artist] = [data['id']]
    return artist_counts, artist_to_ids, metadata_index

artfile = open('downsized_art.json', 'r')
artist_counts, artist_to_ids, metadata_index = get_artist_counts(artfile)
artist_names = artist_counts.keys()
artist_names.sort(key=lambda x: -artist_counts[x])
print artist_names[0]

lookup_file = open('train_val_test_lookup.json', 'r')
train_val_test_lookup = json.load(lookup_file)

top_artists = artist_names[0:28]
top_artists.pop(10)
top_artists.pop(3)
top_artists.pop(0)

# ids_to_keep = []
outfile = open('generate_data.sh', 'w')

for artist in top_artists:
	for oid in artist_to_ids[artist]:
		#oid = oid[:-4]
		if (oid + '.jpg') not in train_val_test_lookup:
			print oid
			continue
		dirname = train_val_test_lookup[oid + '.jpg'] # e.g. 'train'
		s = "cp " + "'old_data/" + dirname + '/' + oid + ".jpg' " + "'data/" + dirname + '/' + oid + ".jpg'\n"
		outfile.write(s.encode("UTF-8"))
