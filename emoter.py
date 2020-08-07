import numpy as np
import cv2

img_file = input("Image File?\n")
img = cv2.imread(img_file, cv2.IMREAD_UNCHANGED)
height, width, channels = img.shape

do_input = "y"
while do_input == "y":
    sprite_size = int(input("Individual sprite size? Default: 256\n") or "256")
    size = int(int(input("Crop size? Default: 96\n") or "96"))
    half_size = int(size/2)
    print("Crop position?")
    pos_x = int(input("X: "))
    pos_y = int(input("Y: "))

    preview = img[
              pos_y - half_size     : pos_y + half_size,
              pos_x - half_size     : pos_x + half_size
              ]
    cv2.imshow("Emote Preview", preview)
    cv2.waitKey(0)
    do_input = input("Based on that preview, do you wish to change your input parameters? (y/n)")

for i in range(0, int((height-offset)/256)):
    for j in range(0, int(width/256)):
        crop_img = img[
                   pos_y - half_size + i * sprite_size  : pos_y + half_size + i * sprite_size,
                   pos_x - half_size + j * sprite_size  : pos_x + half_size + j * sprite_size
                   ]

        cv2.imwrite(img_file[:-4] + "_" + str(i) + "_" + str(j) + img_file[-4:], crop_img)

cv2.waitKey(0)