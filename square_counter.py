import cv2
import numpy as np

# Processing Constants
CANNY_LOWER_THRESHOLD = 150
CANNY_UPPER_THRESHOLD = 255
CANNY_APERTURE_SIZE = 3

HOUGH_RHO = 1
HOUGH_THETA = np.pi / 180
HOUGH_THRESHOLD = 150
HOUGH_MIN_LINE_LENGTH = 150
HOUGH_MAX_LINE_GAP = 7

LINE_ANGLE_TOLERANCE = 5
LINE_DUPLICATE_THRESHOLD = 5


def filter_coords(coords):
    coords = sorted(set(coords))
    # Initialize the filtered coordinates list
    filtered_coords = []
    for coord in coords:
        if filtered_coords and abs(coord - filtered_coords[-1]) <= LINE_DUPLICATE_THRESHOLD:
            # Average the two coordinates and replace the last one
            filtered_coords[-1] = int((filtered_coords[-1] + coord) / 2)
        else:
            # Add the coordinate to the filtered list
            filtered_coords.append(int(coord))
    return filtered_coords


def get_grid_squares():
    # Load the image using cv2
    image_path = r"C:\Users\Lucas\Documents\Crossword_Parser\straightened_image.png"
    # print the size of the image
    print("Image size:", cv2.imread(image_path).shape)
    image = cv2.imread(image_path)

    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # ******TESTING using trackbars******
    # import time
    # import thresholding as th
    # Apply edge detection
    # edges = cv2.Canny(gray, 50, 150, apertureSize=3)
    # canny_trackbar = th.Trackbar(gray, 3, [50, 150, 5], 'canny', 'edges')
    # hough_trackbar = th.Trackbar(edges, 5, [1, 1, 100, 150, 5], 'houghlines', 'houghlines')
    #
    # # canny_draw = image.copy()
    # cv2.namedWindow('Drawn Edges', cv2.WINDOW_KEEPRATIO)
    # cv2.imshow('Drawn Edges', edges)
    # cv2.resizeWindow('Drawn Edges', 500, 500)
    #
    # hough_draw = image.copy()
    # cv2.namedWindow('Drawn Lines', cv2.WINDOW_KEEPRATIO)
    # cv2.imshow('Drawn Lines', hough_draw)
    # cv2.resizeWindow('Drawn Lines', 500, 500)
    #
    # while True:
    #
    #     edges = canny_trackbar.update_image()
    #     if edges is not None:
    #         cv2.imshow('Drawn Edges', edges)
    #         hough_trackbar.update_modifier(edges)
    #
    #     lines = hough_trackbar.update_image()
    #     hough_draw = image.copy()
    #     if lines is not None:
    #         for line in lines:
    #             x1, y1, x2, y2 = line[0]
    #             cv2.line(hough_draw, (x1, y1), (x2, y2), (0, 255, 0), 2)
    #         cv2.imshow('Drawn Lines', hough_draw)
    #         if cv2.waitKey(1) & 0xFF == ord('q'):
    #             break
    #     time.sleep(0.1)
    # ******TESTING using trackbars******

    edges = cv2.Canny(gray, CANNY_LOWER_THRESHOLD, CANNY_UPPER_THRESHOLD, apertureSize=CANNY_APERTURE_SIZE)
    lines = cv2.HoughLinesP(edges, HOUGH_RHO, HOUGH_THETA, threshold=HOUGH_THRESHOLD,
                            minLineLength=HOUGH_MIN_LINE_LENGTH, maxLineGap=HOUGH_MAX_LINE_GAP)

    # Initialize lists to hold the x and y coordinates of the grid lines
    x_coords = []
    y_coords = []

    # Iterate over the detected lines
    for line in lines:
        x1, y1, x2, y2 = line[0]
        if abs(x1 - x2) < LINE_ANGLE_TOLERANCE:  # vertical line (almost same x)
            x_coords.append(x1)
        if abs(y1 - y2) < LINE_ANGLE_TOLERANCE:  # horizontal line (almost same y)
            y_coords.append(y1)

    # Remove duplicates and sort the coordinates
    x_coords = filter_coords(x_coords)

    # Remove duplicates and sort the coordinates
    y_coords = filter_coords(y_coords)

    # Calculate the grid size
    grid_cols = len(x_coords) - 1  # Number of vertical lines - 1 gives us the number of columns
    grid_rows = len(y_coords) - 1  # Number of horizontal lines - 1 gives us the number of rows

    # Calculate cell width and height
    cell_width = (x_coords[-1] - x_coords[0]) // grid_cols
    cell_height = (y_coords[-1] - y_coords[0]) // grid_rows
    print(f"Cell width: {cell_width}, Cell height: {cell_height}")

    # Create a list to hold the coordinates of each square in the grid
    grid_coordinates = []

    # Iterate through the grid and store the coordinates
    for row in range(grid_rows):
        for col in range(grid_cols):
            left = x_coords[col]
            upper = y_coords[row]
            right = x_coords[col + 1]
            lower = y_coords[row + 1]
            grid_coordinates.append((left, upper, right, lower))

    # Output the grid size and the first 10 grid coordinates
    print(f"Detected Grid Size: {grid_rows}x{grid_cols}")
    print("First 10 grid coordinates:", grid_coordinates[:10])

    squares = []
    # If you want to save each square as a separate image:
    for i, coords in enumerate(grid_coordinates):
        left, upper, right, lower = coords
        square = image[upper:lower, left:right]
        squares.append(square)
    return squares