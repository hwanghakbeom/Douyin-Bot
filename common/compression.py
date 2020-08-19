from PIL import Image
import math
import os
import numpy as np
import cv2

def resize_image(origin_img, optimize_img, threshold):
    """
    shrink image by size
    :param origin_img:
    :param optimize_img:
    :param threshold:
    :return:
    """
    file_size = os.path.getsize(origin_img)
    with Image.open(origin_img) as im:
        if file_size > threshold:
            width, height = im.size

            if width >= height:
                new_width = int(math.sqrt(threshold / 2))
                new_height = int(new_width * height * 1.0 / width)
            else:
                new_height = int(math.sqrt(threshold / 2))
                new_width = int(new_height * width * 1.0 / height)

            resized_im = im.resize((new_width, new_height))
            resized_im.save(optimize_img)
        else:
            im.save(optimize_img)



def detect_color(color,img)

#img = cv2.imread('J9MbW.jpg')

brown = [235, 20, 20]  # RED


diff = 20
boundaries = [([brown[2]-diff, brown[1]-diff, brown[0]-diff],
               [brown[2]+diff, brown[1]+diff, brown[0]+diff])]
# in order BGR as opencv represents images as numpy arrays in reverse order

for (lower, upper) in boundaries:
    lower = np.array(lower, dtype=np.uint8)
    upper = np.array(upper, dtype=np.uint8)
    mask = cv2.inRange(img, lower, upper)
    output = cv2.bitwise_and(img, img, mask=mask)

    ratio_brown = cv2.countNonZero(mask)/(img.size/3)
    print('brown pixel percentage:', np.round(ratio_brown*100, 2))
    return np.round(ratio_brown*100, 2)

