import os
from PIL import Image

def process_directory(data_path, output_path):
    filenames = os.listdir(data_path)
    for filename in filenames:
        image = Image.open(os.path.join(data_path, filename))
        small_image = image.resize((224, 224), Image.ANTIALIAS)
        
        image_no_crop_class = Image.new(mode='RGB', size=small_image.size)
        image_no_crop_class.im = small_image.im
        image_no_crop_class.save(os.path.join(output_path, filename), quality=100)

input_dir = 'big_data'
output_dir = 'data'
for data_type in ['train', 'val', 'test']:
    input_path = os.path.join(input_dir, data_type)
    output_path = os.path.join(output_dir, data_type)
    process_directory(input_path, output_path)
