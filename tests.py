import unittest

import square_counter as sc

GRID_15_BY_15 = 225
CORRECT_SQUARE_COUNTS = [(20, 15), (44, 15), (0, 0), (0, 2), (8, 3), (1, 20), (31, 11), (50, 15), (0, 0), (4, 10),
                         (8, 4), (21, 0)]

class TestSquareCounter(unittest.TestCase):
    TEST_IMAGE_PATH = r"C:\Users\Lucas\Documents\Crosswords\Cropped Images"

    def test_grid_squares(self):
        expected_square_count = 225
        for image_number in range(12):
            if image_number == 2 or image_number == 20:
                continue
            with self.subTest(image_number=image_number):
                squares = sc.get_grid_squares(self.TEST_IMAGE_PATH + fr"\grid_image{image_number}.png")
                self.assertEqual(len(squares), GRID_15_BY_15,
                                 f"Failed for image number {image_number}. Expected {GRID_15_BY_15}, got {len(squares)}")

if __name__ == '__main__':
    unittest.main()


#     def test_15x15_grid(self, image_number):
#         squares = sc.get_grid_squares(TEST_IMAGE_PATH + fr"\grid_image{image_number}.png")
#         self.assertEqual(len(squares), GRID_15_BY_15)
#
#     def test_15x15_image(self, image_number, red_squares_count, blue_squares_count):
#         squares = sc.get_grid_squares(
#             rf"C:\Users\Lucas\Documents\Crosswords\Cropped Images\grid_image{image_number}.png")
#         red_squares, blue_squares, normal_squares, black_squares = sc.count_squares(squares)
#         self.assertEqual(len(red_squares), red_squares_count)
#         self.assertEqual(len(blue_squares), blue_squares_count)
#
#
# IMAGE_PATH = r"C:\Users\Lucas\Documents\Crosswords\Cropped Images"
# if __name__ == '__main__':
#     tester = TestSquareCounter()
#     tester.test_15x15_grid(0)
#     # for i in range(11):
#     #     if i == 2 or i == 20:
#     #         continue
#     #     tester.test_15x15_grid(i)
#     #     tester.test_15x15_image(i, CORRECT_SQUARE_COUNTS[i][0], CORRECT_SQUARE_COUNTS[i][1])
