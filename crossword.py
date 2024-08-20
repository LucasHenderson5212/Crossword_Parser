import cv2
import image_parser
import square_counter


class Crossword:
    def __init__(self, image_path):
        self.full_image = cv2.imread(image_path)
        self.__grid_image = image_parser.get_crossword_image(self.full_image)
        self.__date = image_parser.get_date(image_path.split('\\')[-1])
        self.squares = square_counter.get_grid_squares(self.__grid_image)
        self.red_squares, self.blue_squares, self.normal_squares, self.black_squares = square_counter.count_squares(
            self.squares)

    def get_red_square_count(self):
        return len(self.red_squares)

    def get_blue_square_count(self):
        return len(self.blue_squares)

    def get_normal_square_count(self):
        return len(self.normal_squares)

    def get_black_square_count(self):
        return len(self.black_squares)

    def get_date(self):
        return self.__date.replace()

    def set_date(self, date):
        self.__date = date
