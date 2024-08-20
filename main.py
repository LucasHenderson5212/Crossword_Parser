import square_counter as sc
import cv2


def show_image(image, window_name='window'):
    cv2.namedWindow(window_name, cv2.WINDOW_KEEPRATIO)
    cv2.imshow(window_name, image)
    cv2.resizeWindow(window_name, 500, 500)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


IMAGE_PATH = r"C:\Users\Lucas\Documents\Crosswords\Cropped Images"
if __name__ == '__main__':
    for i in range(23):
        path = rf"\grid_image{i}.png"
        img = cv2.imread(IMAGE_PATH + path)
        squares = sc.get_grid_squares(img)
        sc.count_squares(squares)
        show_image(img)

    # image_path = r"C:\Users\Lucas\Documents\Crosswords\Cropped Images\grid_image13.png"
    # img = cv2.imread(image_path)
    # show_image(img)
    # squares = sc.get_grid_squares(img)
    # sc.count_squares(squares)
