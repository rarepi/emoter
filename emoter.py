import numpy as np
import cv2


def make_emotes(img_file, sprite_size, x, y, emote_size):
    print(img_file, sprite_size, x, y, emote_size)
    img = cv2.imread(img_file, cv2.IMREAD_UNCHANGED)
    image_height, image_width, channels = img.shape

    for i in range(0, int(image_height / sprite_size)):
        for j in range(0, int(image_width / sprite_size)):
            crop_img = img[
                       y + i * sprite_size: y + emote_size + i * sprite_size,
                       x + j * sprite_size: x + emote_size + j * sprite_size
                       ]

            cv2.imwrite(img_file[:-4] + "_" + str(i) + "_" + str(j) + img_file[-4:], crop_img)


def main():
    img_file = input("Image File?\n")
    img = cv2.imread(img_file, cv2.IMREAD_UNCHANGED)

    while True:
        sprite_size = int(input("Individual sprite size? Default: 256\n") or "256")
        size = int(int(input("Crop size? Default: 96\n") or "96"))
        half_size = int(size / 2)
        print("Crop position?")
        pos_x = int(input("X: "))
        pos_y = int(input("Y: "))

        preview = img[
                  pos_y - half_size: pos_y + half_size,
                  pos_x - half_size: pos_x + half_size
                  ]
        cv2.imshow("Emote Preview", preview)
        cv2.waitKey(0)
        if input("Based on that preview, do you wish to change your input parameters? (y/n)") != "y":
            break

    make_emotes(img, sprite_size, pos_x - half_size, pos_y - half_size, size)
    cv2.waitKey(0)


if __name__ == "__main__":
    main()
