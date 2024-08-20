import square_counter as sc
import cv2
import file_importer as fi
import image_parser as ip
import thresholding as th


def show_image(image, window_name='window'):
    cv2.namedWindow(window_name, cv2.WINDOW_KEEPRATIO)
    cv2.imshow(window_name, image)
    cv2.resizeWindow(window_name, 500, 500)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


IMAGE_PATH = r"C:\Users\Lucas\Documents\Crosswords\Cropped Images"
if __name__ == '__main__':
    # for i in range(23):
    #     path = rf"\grid_image{i}.png"
    #     squares = sc.get_grid_squares(IMAGE_PATH + path)
    #     sc.count_squares(squares)
    #     show_image(cv2.imread(IMAGE_PATH + path))

    image_path = r"C:\Users\Lucas\Documents\Crosswords\Cropped Images\grid_image13.png"
    show_image(cv2.imread(image_path))
    squares = sc.get_grid_squares(image_path)
    sc.count_squares(squares)

    # images = fi.import_pngs(r"C:\Users\Lucas\Documents\Crosswords\Sorted Scans")

    # good_image = images[0]
    # bad_image1 = images[2]
    # bad_image2 = images[20]

    # bad_images = [good_image, bad_image1, bad_image2]

    # for i, image in enumerate(images):
    #     grid_image = ip.get_crossword_image(image)
    #     #save the grid image
    #     cv2.imwrite(rf"C:\Users\Lucas\Documents\Crosswords\Cropped Images\grid_image{i}.png", grid_image)

    # taskbar = th.Trackbar(image, 6, [90, 200, 50, 160, 49, 130], 'bgr')
    # while True:
    #     mask = taskbar.update_image()
    #     show_image(mask)
    #     cv2.waitKey(1)
