import numpy as np
from PIL import Image
import os 

image_dir = 'data/train'
pixel_sum = np.zeros(shape=(50176, 3))
pixel_sum_sq = np.zeros(shape=(50176, 3))
num_images = 0
for filename in os.listdir(image_dir):
    image = Image.open(os.path.join(image_dir, filename))
    pixels = np.array(image.getdata())
    pixel_sum += pixels
    pixel_sum_sq += (pixels * pixels)
    num_images += 1

pixel_sum = pixel_sum.sum(axis=0)
pixel_sum_sq = pixel_sum_sq.sum(axis=0)

means = pixel_sum / (num_images * 50176)
sum_sq_means = pixel_sum_sq / (num_images * 50176)

stds = np.sqrt(sum_sq_means - (means * means))

print ('Expectations (R, G, B): ' + str(means))
print ('Standard deviations (R, G, B): ' + str(stds))

