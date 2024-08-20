import os
import file_importer as fi
import image_parser as ip
import square_counter as sc

if __name__ == '__main__':
    # fi.sort_and_label(r"C:\Users\Lucas\Documents\Crosswords\Scans")  # only need to preform this once
    sc.get_grid_squares()
    # images = fi.import_pngs(r"C:\Users\Lucas\Documents\Crosswords\Sorted Scans")
    #
    # good_image = images[0]
    # bad_image1 = images[2]
    # bad_image2 = images[20]
    #
    # bad_images = [good_image, bad_image1, bad_image2]
    #
    # for image in bad_images:
    #     ip.get_crossword_image(image)
