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

RED_PIXEL_LOWER_THRESHOLD = (90, 70, 160)
RED_PIXEL_UPPER_THRESHOLD = (140, 160, 255)
RED_PIXEL_COUNT_THRESHOLD = 50

BLUE_PIXEL_LOWER_THRESHOLD = (145, 0, 0)
BLUE_PIXEL_UPPER_THRESHOLD = (255, 255, 130)
BLUE_PIXEL_COUNT_THRESHOLD = 70

BLACK_PIXEL_LOWER_THRESHOLD = (50, 50, 50)
BLACK_PIXEL_UPPER_THRESHOLD = (90, 90, 90)
BLACK_PIXEL_PERCENT_THRESHOLD = 0.90


def show_image(image, window_name='window'):
    cv2.namedWindow(window_name, cv2.WINDOW_KEEPRATIO)
    cv2.imshow(window_name, image)
    cv2.resizeWindow(window_name, 500, 500)

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


def get_grid_squares(image_path):
    image = cv2.imread(image_path)

    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

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
    print(f"Detected Grid Size: {grid_rows}x{grid_cols}\n")

    squares = []
    # If you want to save each square as a separate image:
    for i, coords in enumerate(grid_coordinates):
        left, upper, right, lower = coords
        square = image[upper:lower, left:right]
        squares.append(square)
    return squares


def count_squares(squares):
    red_squares = []
    blue_squares = []
    normal_squares = []
    black_squares = []
    for square in squares:

        red_pixels = cv2.inRange(square, RED_PIXEL_LOWER_THRESHOLD, RED_PIXEL_UPPER_THRESHOLD)
        blue_pixels = cv2.inRange(square, BLUE_PIXEL_LOWER_THRESHOLD, BLUE_PIXEL_UPPER_THRESHOLD)
        black_pixels = cv2.inRange(square, BLACK_PIXEL_LOWER_THRESHOLD, BLACK_PIXEL_UPPER_THRESHOLD)

        red_pixel_count = cv2.countNonZero(red_pixels)
        blue_pixel_count = cv2.countNonZero(blue_pixels)
        black_pixel_count = cv2.countNonZero(black_pixels)
        # print('Red pixel count:', red_pixel_count)
        # print('Blue pixel count:', blue_pixel_count)
        # print('Black pixel count:', black_pixel_count)
        # print('Total pixel count:', square.size/3)
        # print('Black pixel percentage:', black_pixel_count / (square.size / 3))

        if black_pixel_count / (square.size / 3) > BLACK_PIXEL_PERCENT_THRESHOLD:
            print('Black square')
            black_squares.append(square)
        elif red_pixel_count > RED_PIXEL_COUNT_THRESHOLD and blue_pixel_count > BLUE_PIXEL_COUNT_THRESHOLD:
            cv2.imshow('Square', square)
            print('Red and blue square')
            colour = input('Enter the colour of the square: ')
            if colour.lower() == 'red':
                red_squares.append(square)
            elif colour.lower() == 'blue':
                blue_squares.append(square)
            else:
                normal_squares.append(square)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        elif red_pixel_count > RED_PIXEL_COUNT_THRESHOLD:
            print('Red square')
            red_squares.append(square)
        elif blue_pixel_count > BLUE_PIXEL_COUNT_THRESHOLD:
            print('Blue square')
            blue_squares.append(square)
        else:
            print('Normal square')
            normal_squares.append(square)
        print()

    print('Total red squares:', len(red_squares))
    print('Total blue squares:', len(blue_squares))
    print('Total normal squares:', len(normal_squares))
