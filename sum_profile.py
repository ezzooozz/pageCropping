import numpy as np
from scipy import ndimage, misc, stats
from PIL import Image
import sys
import matplotlib.pyplot as plt

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

if __name__ == "__main__":
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    axis = int(sys.argv[3])

    img = ndimage.imread(input_path)
    profile = sum_profile(img, axis)

    maxVal = max(profile) # Absolute max value in profile array
    minVal = min(profile) # Absolute min value in profile array

    avgVal = int((maxVal - minVal) / 2) # This is our threshold value (cut out anything lower than this)

    # print('max: ' + str(maxVal) + ' min: ' + str(minVal) + ' avg: ' + str(avgVal))
    newProfile = stats.threshold(profile, threshmin=avgVal)
    firstNonZeroIndex = next((index for index,value in enumerate(newProfile) if value != 0), None) # Grab the first index of the cropped image
    lastNonZeroIndex = len(newProfile) - next((index for index,value in enumerate(list(reversed(newProfile))) if value != 0), None) # Grab the last index of the cropped image
    # newProfile = newProfile[firstNonZeroIndex:lastNonZeroIndex] # Reform the profile to be just the cropped dimensions.

    pic = Image.open(sys.argv[1])
    w,h = pic.size
    print('Original width ' + str(w) + ' and height ' + str(h))
    pic2 = pic.crop((firstNonZeroIndex, 0, lastNonZeroIndex, h))
    pic2.save(sys.argv[2])

    plt.plot(profile)
    plt.plot(newProfile)
    plt.show()

    #plt.savefig(output_path)
