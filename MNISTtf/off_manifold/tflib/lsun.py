import numpy as np
import scipy.misc
import time
import cv2

from os import listdir

def make_generator(path, n_files, batch_size, image_size):
    epoch_count = [1]
    images_name = listdir(path)
    if n_files == 0:
        n_files = len(images_name)
    else:
        n_files = n_files
    
    def get_epoch():
        images = np.zeros((batch_size, 3, image_size, image_size), dtype='int32')
        files = range(n_files)
        random_state = np.random.RandomState(epoch_count[0])
        random_state.shuffle(files)
        epoch_count[0] += 1
        for n, i in enumerate(files):
            #image = scipy.misc.imread("{}/{}.png".format(path, str(i+1)))
            image = scipy.misc.imread("%s"%(path +'/'+ images_name[i]))
	    image = cv2.resize(image,(image_size,image_size),interpolation = cv2.INTER_AREA)
            images[n % batch_size] = image.transpose(2,0,1)
            if n > 0 and n % batch_size == 0:
                yield (images,)
    return get_epoch

def load(batch_size, data_dir='/home/ishaan/data/imagenet64',image_size = 64, n_files = 0):
    return (
        make_generator(data_dir+'/train', n_files = n_files, batch_size = batch_size, image_size = image_size),
        make_generator(data_dir+'/val', n_files = n_files, batch_size = batch_size, image_size = image_size)
    )

# test data
if __name__ == '__main__':
    train_gen, valid_gen = load(64)
    t0 = time.time()
    for i, batch in enumerate(train_gen(), start=1):
        print("{}\t{}".format(str(time.time() - t0), batch[0][0,0,0,0]))
        if i == 1000:
            break
        t0 = time.time()
