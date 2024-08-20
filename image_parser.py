import cv2
import numpy as np
import datetime


def show_image(image, window_name='window'):
    cv2.namedWindow(window_name, cv2.WINDOW_KEEPRATIO)
    cv2.imshow(window_name, image)
    cv2.resizeWindow(window_name, 500, 500)


# returns the contour outlining the crossword grid
def find_grid(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply GaussianBlur to reduce noise and improve contour detection
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Apply adaptive thresholding to create a binary image
    binary = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)

    # Find contours
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # draw the contours on a copy of the image
    # image_copy = image.copy()
    # cv2.drawContours(image_copy, contours, -1, (0, 255, 0), 3)
    # show_image(image_copy, 'Contours')

    # Initialize variables to store the largest rectangle found
    largest_area = 0
    largest_rect = None
    largest_contour = None

    # Iterate through contours to find the largest rectangle
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        area = w * h
        aspect_ratio = w / float(h)

        # Filter based on area and aspect ratio
        if area > largest_area and 0.8 < aspect_ratio < 1.2:  # assuming the crossword grid is roughly square
            largest_area = area
            largest_rect = (x, y, w, h)
            largest_contour = contour

    if largest_rect:
        return largest_contour

    else:
        print('No crossword grid found')
        return None


# Straighten the image based on the largest contour, returns the original image if no adequate contour is found
def straighten_image(largest_contour, image):
    # Approximate the contour to a polygon
    perimeter = cv2.arcLength(largest_contour, True)
    approx = cv2.approxPolyDP(largest_contour, 0.02 * perimeter, True)

    # If the polygon has 4 points, we assume it is the rectangle
    if len(approx) == 4:
        src_points = np.float32(approx).reshape(-1, 2)

        # Sort the points in the order top-left, top-right, bottom-right, bottom-left
        sorted_points = src_points[np.argsort([np.sum(p) for p in src_points])]
        top_left, bottom_right = sorted_points[[0, -1]]
        top_right, bottom_left = sorted_points[np.argsort([p[1] - p[0] for p in sorted_points])][[0, -1]]

        ordered_points = [top_left, top_right, bottom_right, bottom_left]

        # Define the width and height of the rectangle
        width = int(np.linalg.norm(ordered_points[0] - ordered_points[1]))
        height = int(np.linalg.norm(ordered_points[0] - ordered_points[3]))

        # Define destination points
        dst_points = np.float32([[0, 0], [width - 1, 0], [width - 1, height - 1], [0, height - 1]])
        ordered_points = np.array(ordered_points)
        # Compute the perspective transform matrix and apply it
        matrix = cv2.getPerspectiveTransform(ordered_points, dst_points)
        unskewed_image = cv2.warpPerspective(image, matrix, (width, height))

        return unskewed_image
    else:
        print('grid unsuitable for straightening')
        return image


def get_crossword_image(image):
    contour = find_grid(image)
    if contour is not None:
        grid_image = straighten_image(contour, image)
        # show_image(og_image, 'Original Image')
        # show_image(grid_image, 'Straightened Image')

        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        return grid_image
    else:
        print('No grid found')
        return image


def get_date(image_name):
    image_number = image_name.split('_')[1].split('.')[0]

    # Calculate the date starting from January 1st
    start_date = datetime.date(2024, 1, 1)

    # Initialize counters
    combined_day_count = 0
    current_date = start_date

    while combined_day_count < image_number:
        # Move to the next day
        current_date += datetime.timedelta(days=1)

        # Count combined weekend as a single day
        if current_date.weekday() == 5:  # Saturday
            combined_day_count += 1
            current_date += datetime.timedelta(days=1)  # Skip to Monday
        elif current_date.weekday() == 6:  # Sunday
            continue  # Already counted as part of Saturday
        else:
            combined_day_count += 1

    return current_date
