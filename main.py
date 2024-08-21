import os

import cv2

import crossword

TOTAL_DAYS = 366 - 52


def show_image(image, window_name='window'):
    cv2.namedWindow(window_name, cv2.WINDOW_KEEPRATIO)
    cv2.imshow(window_name, image)
    cv2.resizeWindow(window_name, 500, 500)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


IMAGE_PATH = r"C:\Users\Lucas\Documents\Crosswords\Cropped Images"
CROSSWORDS_PATH = r"C:\Users\Lucas\Documents\Crosswords"
if __name__ == '__main__':
    crosswords = []
    for file in os.listdir(CROSSWORDS_PATH):
        crossword = crossword.Crossword(os.path.join(CROSSWORDS_PATH, file))
        print(crossword.get_date())
        crosswords.append(crossword)
