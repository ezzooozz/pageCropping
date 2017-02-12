import numpy as np
from scipy import ndimage, misc, stats
from PIL import Image
import sys
import matplotlib.pyplot as plt
from skimage.filters.rank import median
from skimage.morphology import disk
from skimage import img_as_float
from scipy import ndimage

HORIZONTAL = 0
VERTICAL = 1

def sum_profile(img, axis=0):
    img = to_gray(img)
    return img.sum(axis=axis)

def to_gray(img):
    if len(img.shape) == 2 or img.shape[2] == 1:
        #Already gray
        return img
    r, g, b = img[:,:,0], img[:,:,1], img[:,:,2]

    gray = 0.2989 * r + 0.5870 * g + 0.1140 * b
    return gray

def crop_profile(original,image, profile, direction):
    maxVal = max(profile) # Absolute max value in profile array
    minVal = min(profile) # Absolute min value in profile array

    avgVal = int((maxVal - minVal) / 2) # This is our threshold value (cut out anything lower than this)

    # print('max: ' + str(maxVal) + ' min: ' + str(minVal) + ' avg: ' + str(avgVal))
    newProfile = stats.threshold(profile, threshmin=avgVal)
    firstNonZeroIndex = next((index for index,value in enumerate(newProfile) if value != 0), None) # Grab the first index of the cropped image
    lastNonZeroIndex = len(newProfile) - next((index for index,value in enumerate(list(reversed(newProfile))) if value != 0), None) # Grab the last index of the cropped image
    # newProfile = newProfile[firstNonZeroIndex:lastNonZeroIndex] # Reform the profile to be just the cropped dimensions.

    w,h = image.size
    print('Original width ' + str(w) + ' and height ' + str(h))
    if(direction == HORIZONTAL):
        pic2 = original.crop((firstNonZeroIndex, 0, lastNonZeroIndex, h))
    else:
        pic2 = original.crop((0, firstNonZeroIndex, w, lastNonZeroIndex))

    return pic2, newProfile


if __name__ == "__main__":
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    # axis = int(sys.argv[3])

    # Transform the original image using a median filter of radius 22px.
    img = ndimage.imread(input_path, flatten=True)
    # img = median(img, disk((60)))
    img = ndimage.gaussian_filter(img, sigma=3)
    # img = ndimage.filters.median_filter(img,size=22)
    # For diagnostics on median filter step
    # misc.imsave('outfile.jpg', img)

    hProfile = sum_profile(img, 0) # Horizontal profile
    vProfile = sum_profile(img, 1) # Vertical profile

    pic = Image.fromarray(img)
    original = Image.open(sys.argv[1])

    '''Horizontal Profile Cropping'''
    pic, newHProfile = crop_profile(original,pic, hProfile, HORIZONTAL)

    '''Vertical Profile Cropping'''
    pic, newVProfile = crop_profile(pic,pic, vProfile, VERTICAL)

    # Save the updated picture object
    pic.save(sys.argv[2])

    plt.figure(0)
    plt.plot(vProfile, label='original')
    plt.plot(newVProfile, label='cropped')
    plt.legend()
    plt.title('Vertical Profile')
    plt.savefig('plotvOutput.png')

    plt.figure(1)
    plt.plot(hProfile, label='original')
    plt.plot(newHProfile, label='cropped')
    plt.title('Horizontal Profile')
    plt.legend()
    plt.savefig('plothOutput.png')
    plt.show()

