import numpy as np
import cv2

img = cv2.imread('J9MbW.jpg')

brown = [235, 20, 20]  # RGB
diff = 20
boundaries = [([brown[2]-diff, brown[1]-diff, brown[0]-diff],
               [brown[2]+diff, brown[1]+diff, brown[0]+diff])]
# in order BGR as opencv represents images as numpy arrays in reverse order
print(boundaries)
for (lower, upper) in boundaries:
    lower = np.array(lower, dtype=np.uint8)
    upper = np.array(upper, dtype=np.uint8)
    mask = cv2.inRange(img, lower, upper)
    output = cv2.bitwise_and(img, img, mask=mask)

    ratio_brown = cv2.countNonZero(mask)/(img.size/3)
    print('brown pixel percentage:', np.round(ratio_brown*100, 2))

    cv2.imshow("images", np.hstack([img, output]))
    cv2.waitKey(0)
