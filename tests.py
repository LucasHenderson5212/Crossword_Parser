import unittest

import square_counter as sc

GRID_15_BY_15 = 225
GRID_16_BY_15 = 240
CORRECT_SQUARE_COUNTS = [(20, 15), (44, 15), (27, 0), (0, 0), (0, 2), (8, 3), (1, 20), (31, 11), (50, 15), (0, 0),
                         (4, 10), (8, 4), (21, 0), (23, 41), (32, 38), (4, 0), (2, 3), (2, 37), (15, 31), (10, 29),
                         (19, 31), (19, 31), (0, 0), (3, 3)]


class TestSquareCounter(unittest.TestCase):
    TEST_IMAGE_PATH = r"C:\Users\Lucas\Documents\Crosswords\Cropped Images"

    def test_grid_squares(self):
        for image_number in range(22):
            if image_number == 2 or image_number == 20:
                continue
            with self.subTest(image_number=image_number):
                squares = sc.get_grid_squares(self.TEST_IMAGE_PATH + fr"\grid_image{image_number}.png")
                if image_number == 6 or image_number == 17:
                    self.assertEqual(len(squares), GRID_16_BY_15,
                                     f"Failed for image number {image_number}."
                                     f"Expected GRID_16_BY_15, got {len(squares)}")
                else:
                    self.assertEqual(len(squares), GRID_15_BY_15,
                                     f"Failed for image number {image_number}. Expected {GRID_15_BY_15},"
                                     f"got {len(squares)}")

    def test_grid_colour_counts(self):
        for image_number in range(22):
            if image_number == 2 or image_number == 20:
                continue
            with self.subTest(image_number=image_number):
                squares = sc.get_grid_squares(self.TEST_IMAGE_PATH + fr"\grid_image{image_number}.png")
                red_squares, blue_squares, normal_squares, black_squares = sc.count_squares(squares)
                self.assertEqual(len(red_squares), CORRECT_SQUARE_COUNTS[image_number][0],
                                 f"Failed for image number {image_number}."
                                 f"Expected {CORRECT_SQUARE_COUNTS[image_number][0]}, got {len(red_squares)}")
                self.assertEqual(len(blue_squares), CORRECT_SQUARE_COUNTS[image_number][1],
                                 f"Failed for image number {image_number}."
                                 f"Expected {CORRECT_SQUARE_COUNTS[image_number][1]}, got {len(blue_squares)}")

                if image_number == 6 or image_number == 17:
                    self.assertEqual(len(red_squares) + len(blue_squares) + len(normal_squares) + len(black_squares),
                                     GRID_16_BY_15, f"Failed for image number {image_number}. Expected {GRID_16_BY_15},"
                                                    f"got {len(red_squares) + len(blue_squares) + len(normal_squares) +
                                                           len(black_squares)}")
                else:
                    self.assertEqual(len(red_squares) + len(blue_squares) + len(normal_squares) + len(black_squares),
                                     GRID_15_BY_15, f"Failed for image number {image_number}. Expected {GRID_15_BY_15},"
                                                    f"got {len(red_squares) + len(blue_squares) + len(normal_squares) +
                                                           len(black_squares)}")


if __name__ == '__main__':
    unittest.main()
