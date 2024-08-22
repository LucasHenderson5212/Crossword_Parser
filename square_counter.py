import tkinter as tk

import cv2
import numpy as np
from PIL import Image, ImageTk

# Processing Constants
CANNY_LOWER_THRESHOLD = 150
CANNY_UPPER_THRESHOLD = 255
CANNY_APERTURE_SIZE = 3

HOUGH_RHO = 1
HOUGH_THETA = np.pi / 180
HOUGH_THRESHOLD = 150
HOUGH_MIN_LINE_LENGTH = 100
HOUGH_MAX_LINE_GAP = 5

LINE_ANGLE_TOLERANCE = 5
LINE_SEPARATION_TOLERANCE = 10

RED_PIXEL_LOWER_THRESHOLD = (90, 70, 160)
RED_PIXEL_UPPER_THRESHOLD = (140, 160, 255)
RED_PIXEL_COUNT_THRESHOLD = 50

BLUE_PIXEL_LOWER_THRESHOLD = (145, 0, 0)
BLUE_PIXEL_UPPER_THRESHOLD = (255, 255, 130)
BLUE_PIXEL_COUNT_THRESHOLD = 60

MIN_COLOUR_PIXEL_COUNT = 3

BLACK_PIXEL_LOWER_THRESHOLD = (50, 50, 50)
BLACK_PIXEL_UPPER_THRESHOLD = (90, 90, 90)
BLACK_PIXEL_PERCENT_THRESHOLD = 0.90

TESTING = False
SHOW_IMAGES = False


def show_image(image, window_name='window', wait=True):
    cv2.namedWindow(window_name, cv2.WINDOW_KEEPRATIO)
    cv2.imshow(window_name, image)
    cv2.resizeWindow(window_name, 500, 500)
    if wait:
        cv2.waitKey(0)
        cv2.destroyAllWindows()


def trackbar_test(gray, image):
    import time
    import thresholding as th
    # Apply edge detection
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)
    canny_trackbar = th.Trackbar(gray, 3, [CANNY_LOWER_THRESHOLD, CANNY_UPPER_THRESHOLD, CANNY_APERTURE_SIZE], 'canny',
                                 'edges')
    hough_trackbar = th.Trackbar(edges, 5, [HOUGH_RHO, int(HOUGH_THETA * 180 / np.pi), HOUGH_THRESHOLD,
                                            HOUGH_MIN_LINE_LENGTH, HOUGH_MAX_LINE_GAP], 'houghlines', 'houghlines')

    # canny_draw = image.copy()
    cv2.namedWindow('Drawn Edges', cv2.WINDOW_KEEPRATIO)
    cv2.imshow('Drawn Edges', edges)
    cv2.resizeWindow('Drawn Edges', 500, 500)

    hough_draw = image.copy()
    cv2.namedWindow('Drawn Lines', cv2.WINDOW_KEEPRATIO)
    cv2.imshow('Drawn Lines', hough_draw)
    cv2.resizeWindow('Drawn Lines', 500, 500)

    while True:

        edges = canny_trackbar.update_image()
        if edges is not None:
            cv2.imshow('Drawn Edges', edges)
            hough_trackbar.update_modifier(edges)

        lines = hough_trackbar.update_image()
        hough_draw = image.copy()
        if lines is not None:
            for line in lines:
                x1, y1, x2, y2 = line[0]
                cv2.line(hough_draw, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.imshow('Drawn Lines', hough_draw)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        time.sleep(0.1)


def filter_coords(coords):
    coords = sorted(set(coords))
    # Initialize the filtered coordinates list
    filtered_coords = []
    for coord in coords:
        if filtered_coords and abs(coord - filtered_coords[-1]) <= LINE_SEPARATION_TOLERANCE:
            # Average the two coordinates and replace the last one
            filtered_coords[-1] = int((filtered_coords[-1] + coord) / 2)
        else:
            # Add the coordinate to the filtered list
            filtered_coords.append(int(coord))
    return filtered_coords


def show_image_with_input(image):
    # Create a Tkinter window
    root = tk.Tk()
    root.title("Image with Input")

    # Convert the image to a format Tkinter can use
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image_pil = Image.fromarray(image_rgb)
    image_tk = ImageTk.PhotoImage(image_pil)

    # Create a label to display the image
    label = tk.Label(root, image=image_tk)  # type: ignore
    label.pack()

    # Create an entry widget for text input
    entry = tk.Entry(root)
    entry.pack()

    # Variable to store the input
    user_input = tk.StringVar()

    # Define a callback function to save the input and close the window
    def on_submit():
        user_input.set(entry.get())
        root.destroy()

    # Create a button to submit the input
    button = tk.Button(root, text="Submit", command=on_submit)
    button.pack()

    # Run the Tkinter main loop
    root.mainloop()

    # Return the input
    return user_input.get()


def get_grid_squares(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    if TESTING:
        trackbar_test(gray, image)

    edges = cv2.Canny(gray, CANNY_LOWER_THRESHOLD, CANNY_UPPER_THRESHOLD, apertureSize=CANNY_APERTURE_SIZE)
    lines = cv2.HoughLinesP(edges, HOUGH_RHO, HOUGH_THETA, threshold=HOUGH_THRESHOLD,
                            minLineLength=HOUGH_MIN_LINE_LENGTH, maxLineGap=HOUGH_MAX_LINE_GAP)

    if SHOW_IMAGES:
        # draw and show lines
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
        show_image(image, 'Lines')

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
    # Output the grid size and the first 10 grid coordinates
    print(f"Detected Grid Size (height x width): {grid_rows}x{grid_cols}\n")

    if SHOW_IMAGES:
        draw_img = image.copy()
        for coord in x_coords:
            cv2.circle(draw_img, (coord, y_coords[1]), 8, (0, 150, 255), -1)
        for coord in y_coords:
            cv2.circle(draw_img, (x_coords[1], coord), 5, (0, 0, 255), -1)
        show_image(draw_img, 'Circles')

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
        print('Red pixel count:', red_pixel_count)
        print('Blue pixel count:', blue_pixel_count)
        # print('Black pixel count:', black_pixel_count)
        # print('Total pixel count:', square.size/3)
        # print('Black pixel percentage:', black_pixel_count / (square.size / 3))

        if black_pixel_count / (square.size / 3) > BLACK_PIXEL_PERCENT_THRESHOLD:
            print('Black square')
            black_squares.append(square)
        elif red_pixel_count > RED_PIXEL_COUNT_THRESHOLD:
            print('Red square')
            red_squares.append(square)
        elif blue_pixel_count > BLUE_PIXEL_COUNT_THRESHOLD:
            print('Blue square')
            blue_squares.append(square)
        elif red_pixel_count > MIN_COLOUR_PIXEL_COUNT or blue_pixel_count > MIN_COLOUR_PIXEL_COUNT:
            print('Red pixel count:', red_pixel_count)
            print('Blue pixel count:', blue_pixel_count)
            print('Unsure. [c]ontinue to prompt')
            # show_image(square, "Prompt image", False)
            # cv2.namedWindow("Prompt image", cv2.WINDOW_KEEPRATIO)
            # cv2.imshow("Prompt image", square)
            # cv2.resizeWindow("Prompt image", 500, 500)
            # while True:
            #     if cv2.waitKey(1) & 0xFF == ord('c'):
            #         break
            #     if cv2.getWindowProperty("Prompt image", cv2.WND_PROP_VISIBLE) < 1:
            #         break
            # colour = input('Enter the colour of the square ([n]ormal, [b]lue, [r]ed): ')
            # cv2.destroyAllWindows()
            colour = 'None'
            if colour.lower() == 'r':
                red_squares.append(square)
            elif colour.lower() == 'b':
                blue_squares.append(square)
            elif colour.lower() == 'n':
                normal_squares.append(square)
            else:
                normal_squares.append(square)
        else:
            print('Normal square')
            normal_squares.append(square)
        # show_image(square)
        # print()

    print('Total red squares:', len(red_squares))
    print('Total blue squares:', len(blue_squares))
    print('Total black squares:', len(black_squares))
    print('Total normal squares:', len(normal_squares))
    print()

    # if len(red_squares) != 23:
    #     for square in red_squares:
    #         show_image(square, 'Red square')
    #     for square in normal_squares:
    #         show_image(square, 'Normal square')

    return red_squares, blue_squares, normal_squares, black_squares
