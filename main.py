import square_counter as sc
import cv2
import thresholding as th


def show_image(image, window_name='window'):
    cv2.namedWindow(window_name, cv2.WINDOW_KEEPRATIO)
    cv2.imshow(window_name, image)
    cv2.resizeWindow(window_name, 500, 500)


if __name__ == '__main__':
    squares = sc.get_grid_squares(r"C:\Users\Lucas\Documents\Crossword_Parser\straightened_image.png")
    image = cv2.imread(r"C:\Users\Lucas\Documents\Crossword_Parser\straightened_image.png")
    sc.count_squares(squares)
    # taskbar = th.Trackbar(image, 6, [90, 200, 50, 160, 49, 130], 'bgr')
    # while True:
    #     mask = taskbar.update_image()
    #     show_image(mask)
    #     cv2.waitKey(1)
