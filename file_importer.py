import os
import shutil

import cv2


def sort_and_label(folder):
    # Get the list of files in the folder
    files = os.listdir(folder)

    for file in files:
        if len(file.split('_')) != 3:
            new_name = 'Scan_000.png'
        else:
            name = file.split('.')[0]
            number = name.split('_')[2]
            new_name = f"Scan_{number.zfill(3)}.png"

        source_path = os.path.join(folder, file)
        destination_path = os.path.join(r"C:\Users\Lucas\Documents\Crosswords\Sorted Scans", new_name)

        # Copy the file to the new destination
        shutil.copy(source_path, destination_path)


def import_pngs(folder):
    images = []

    # Get the list of files in the folder
    files = os.listdir(folder)

    for file in files:
        if file.endswith('.png'):
            path = os.path.join(folder, file)
            img = cv2.imread(path)
            height, width = img.shape[:2]
            images.append(img[0:height//2, 0:width])  # crop the image to the top half due to scanning in as letter size

    return images
