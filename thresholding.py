import cv2
import numpy as np


class Trackbar:
    def __init__(self, img, number_of_thresholds=1, threshold_type='HSV'):
        self.default_lower_threshold = 11
        self.default_upper_threshold = 22
        self.lower_threshold = np.array([])
        self.upper_threshold = np.array([])
        self.lower_trackbar_names = []
        self.upper_trackbar_names = []
        self.img = img
        self.number_of_thresholds = number_of_thresholds
        self.type = threshold_type

        for i in range(number_of_thresholds):
            self.lower_threshold = np.append(self.lower_threshold, self.default_lower_threshold)
            self.upper_threshold = np.append(self.upper_threshold, self.default_upper_threshold)

        self.window_name = "Threshold Calibrator"
        cv2.namedWindow(self.window_name, cv2.WINDOW_KEEPRATIO)

        if threshold_type == 'HSV':
            self.upper_trackbar_names.extend(['Upper Hue', 'Upper Sat', 'Upper Val'])
            self.lower_trackbar_names.extend(['Lower Hue', 'Lower Sat', 'Lower Val'])
        elif threshold_type == 'RGB':
            self.upper_trackbar_names.extend(['Upper Red', 'Upper Green', 'Upper Blue'])
            self.lower_trackbar_names.extend(['Lower Red', 'Lower Green', 'Lower Blue'])
        elif threshold_type == 'binary':
            self.upper_trackbar_names.append('MaxVal')
            self.lower_trackbar_names.append('Thresh')
        elif threshold_type == 'adaptive':
            self.upper_trackbar_names.append('C')
            self.lower_trackbar_names.append('Block Size')

        # create trackbars for thresholding
        for i in range(number_of_thresholds):
            cv2.createTrackbar(self.upper_trackbar_names[i], self.window_name, 0, 40, self.on_trackbar)
            cv2.setTrackbarPos(self.upper_trackbar_names[i], self.window_name, self.default_upper_threshold)

            cv2.createTrackbar(self.lower_trackbar_names[i], self.window_name, 0, 20, self.on_trackbar)
            cv2.setTrackbarPos(self.lower_trackbar_names[i], self.window_name, self.default_lower_threshold)

    def on_trackbar(self, val):
        # This function is called whenever the trackbar value changes
        pass

    def update_image(self):
        for i in range(self.number_of_thresholds):
            self.upper_threshold[0] = cv2.getTrackbarPos(self.upper_trackbar_names[i], self.window_name)
            self.lower_threshold[0] = cv2.getTrackbarPos(self.lower_trackbar_names[i], self.window_name)

        if self.type == 'HSV':
            mask = cv2.inRange(cv2.cvtColor(self.img, cv2.COLOR_BGR2HSV), (self.lower_threshold[0],
                                                                           self.lower_threshold[1],
                                                                           self.lower_threshold[2]),
                               (self.upper_threshold[0], self.upper_threshold[1], self.upper_threshold[2]))
        elif self.type == 'RGB':
            mask = cv2.inRange(self.img, (self.lower_threshold[0], self.lower_threshold[1], self.lower_threshold[2]),
                               (self.upper_threshold[0], self.upper_threshold[1], self.upper_threshold[2]))
        elif self.type == 'binary':
            _, mask = cv2.threshold(self.img, int(self.lower_threshold[0]), int(self.upper_threshold[0]),
                                    cv2.THRESH_BINARY)
        elif self.type == 'adaptive':
            if self.lower_threshold[0] % 2 == 0:
                self.lower_threshold[0] += 1
            self.upper_threshold[0] = self.upper_threshold[0] - 20
            mask = cv2.adaptiveThreshold(self.img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,
                                         int(self.lower_threshold[0]), int(self.upper_threshold[0]))
        else:
            print('Invalid threshold type')
            return

        cv2.imshow(self.window_name, mask)
        cv2.resizeWindow(self.window_name, 500, 500)

        return mask
