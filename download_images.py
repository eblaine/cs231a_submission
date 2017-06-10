# import pymongo
import requests
from scipy import ndimage, misc
from io import BytesIO
import matplotlib.pyplot as plt
import numpy as np
from six.moves import cPickle as pickle
import platform

# client = pymongo.MongoClient()
# db = client.rijks
n = 10
currIndex = 0
currBatch = 0
datadict = {'data': np.zeros(shape=(n, 3, 256, 256)), 'labels': []}
filename_base = 'data/data_batch_'

def resize_image(img):
	# get shape of image
	H, W, C = img.shape

	# determine whether length or width is smaller
	bigger = max(H, W)
	smaller = min(H, W)
	ratio = float(bigger) / float(smaller)

	# resize to make smaller dimension 256
	if H > W:
		shape = (int(256 * ratio), 256, C)
	else: 
		shape = (256, int(256 * ratio), C)

	resized = misc.imresize(img, shape)

	# crop larger dimension using middle 256 elements
	re_H, re_W, re_c = resized.shape
	# print 'resized', re_H, re_W

	#row_start_index = re_H/2 - 128
	#col_start_index = re_W/2 - 128
	center_x, center_y = (re_W / 2, re_H / 2)
	# print 'center indices', center_x, center_y
	left_side = center_x - 128
	top = center_y - 128

	# print 'left indices', left_side, top
	center_crop = resized[top:top+256, left_side:left_side+256]
	#center_crop = resized[row_start_index:row_start_index+256, col_start_index:col_start_index+256]
	# print center_crop.shape	


	# small_image = img 
	# if smaller_dim > 256:
	# 	small_image = block_mean(img, smaller_dim / 256)
	# print small_image.shape
	# center_x, center_y = (len(small_image[0]) / 2, len(small_image) / 2)
	# left_side = center_x - 128
	# top = center_y - 128
	# center_crop = small_image[left_side:left_side+256][top:top+256]
	# print center_crop.shape

	return center_crop, resized


# utility function for later!
def get_rgb(url):
	try:	
		r = requests.get(url)
	except requests.exceptions.ConnectionError:
		return []
	
	# full image, needs downsampling to 256 x 256
	full_image = ndimage.imread(BytesIO(r.content))
	crop, small_image = resize_image(full_image)

	return crop / 256., small_image / 256.

def save_image(cropped, resized, obj_id, currIndex):
	# try: 
	# 	db.images.insert({'obj_id': obj_id, 'cropped': cropped, 'downsampled': resized})
	# except pymongo.errors.DuplicateKeyError:
	# 	return
	# plt.imshow(resized)
	# plt.show()

	# save as N x C x H x W


	datadict['data'][currIndex, :, :, :] = cropped.transpose(2, 0, 1)
	datadict['labels'].append(obj_id)

def load_pickle(f):
    version = platform.python_version_tuple()
    if version[0] == '2':
        return  pickle.load(f)
    elif version[0] == '3':
        return  pickle.load(f, encoding='latin1')
    raise ValueError("invalid python version: {}".format(version))

def pickle_and_next_batch(currBatch):
	f = open(filename_base + str(currBatch), 'w')
	pickle.dump(datadict, f)
	f.close()

def load_batch_test(filename):
	with open(filename, 'rb') as f:
		datadict = load_pickle(f)
		X = datadict['data']
		Y = datadict['labels']
		X = X.reshape(n, 3, 256, 256).transpose(0,2,3,1).astype("float")
		X = X.transpose(0, 3, 1, 2) # N H W C --> N C H W	
		return X, Y

# load_batch_test(filename_base + str(0))

# for painting_json in db.art.find():
# 	url = painting_json.get('url')
# 	if url != '':
# 		img = get_rgb(url)
# 		if img == []:
# 			continue
# 		cropped, resized = img
# 		if currIndex >= n:
# 			pickle_and_next_batch(currBatch)
# 			currBatch += 1
# 			currIndex = 0
# 			print currBatch

# 		save_image(cropped, resized, painting_json.get('obj_id'), currIndex)
# 		currIndex += 1
with open('painting_urls.tsv', 'r') as f:
	print len(f.readlines())
# 			