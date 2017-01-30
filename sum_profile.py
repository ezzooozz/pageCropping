import numpy as np
from scipy import ndimage, misc
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
    furthestTrough = 0
    pixelsIn = 0
    peaked = False
    for val in profile:
        if val >= furthestTrough and peaked == False:
            furthestTrough = val
        else:
            peaked = True
            if val < furthestTrough:
                furthestTrough = val
            else:
                break
        pixelsIn += 1

    troughs = np.r_[True, profile[1:] < profile[:-1]] & np.r_[profile[:-1] < profile[1:], True]
    # print(troughs)

    spot = 0
    # for tru in troughs:
        # if tru == True:
            # print(spot)
        # spot += 1

    pic = Image.open(sys.argv[1])
    w,h = pic.size
    print('width: ' + str(w) + ' height: ' + str(h))
    pic2 = pic.crop(((pixelsIn + (w/100)), 0, w, h))
    pic2.save(sys.argv[2])

    plt.plot(profile[int(pixelsIn + (w/100)):])
    plt.show()
    #plt.savefig(output_path)
