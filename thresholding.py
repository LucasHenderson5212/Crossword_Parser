import cv2
import numpy as np


class Trackbar:
    def __init__(self, input_source, number_of_parameters=1, default_parameters=None, threshold_type='binary',
                 window_name='Threshold Calibrator'):
        if default_parameters is None:
            default_parameters = [0] * number_of_parameters
        self.modifier = input_source
        self.number_of_parameters = number_of_parameters
        self.type = threshold_type
        self.parameters = default_parameters
        self.trackbar_names = []
        self.trackbar_limits = []
        self.window_name = window_name

        cv2.namedWindow(self.window_name, cv2.WINDOW_KEEPRATIO)

        if threshold_type == 'binary':
            self.trackbar_names = ['Thresh', 'MaxVal']
            self.trackbar_limits = [(1, 255), (1, 255)]
        elif threshold_type == 'adaptive':
            self.trackbar_names = ['Block Size', 'C']
            self.trackbar_limits = [(1, 255), (-255, 255)]
        elif threshold_type == 'houghlines':
            self.trackbar_names = ['Rho', 'Theta', 'Threshold', 'Min Line Length', 'Max Line Gap']
            self.trackbar_limits = [(1, 50), (1, 180), (1, 500), (1, 500), (1, 50)]
        elif threshold_type == 'canny':
            self.trackbar_names = ['Lower Threshold', 'Upper Threshold', 'Aperture Size']
            self.trackbar_limits = [(1, 255), (1, 255), (3, 7)]

        # create trackbars for thresholding
        for i in range(self.number_of_parameters):
            # cv2.createTrackbar(self.trackbar_names[i], self.window_name, self.trackbar_limits[i][0],
            #                    self.trackbar_limits[i][1], self.on_trackbar)
            cv2.createTrackbar(self.trackbar_names[i], self.window_name, self.parameters[i], self.trackbar_limits[i][1],
                               self.on_trackbar)

    def on_trackbar(self, val):
        # This function is called whenever the trackbar value changes
        pass

    def update_modifier(self, new_modifier):
        self.modifier = new_modifier

    def update_image(self):
        for i in range(self.number_of_parameters):
            self.parameters[i] = cv2.getTrackbarPos(self.trackbar_names[i], self.window_name)
            if self.parameters[i] < self.trackbar_limits[i][0]:
                self.parameters[i] = self.trackbar_limits[i][0]
                cv2.setTrackbarPos(self.trackbar_names[i], self.window_name, self.parameters[i])

        if self.type == 'binary':
            _, filter_applied = cv2.threshold(self.modifier, self.parameters[0], self.parameters[1], cv2.THRESH_BINARY)
        elif self.type == 'adaptive':
            if self.parameters[0] % 2 == 0:
                self.parameters[0] -= 1
                cv2.setTrackbarPos(self.trackbar_names[0], self.window_name, self.parameters[0])
            self.parameters[1] = self.parameters[1] - 20
            filter_applied = cv2.adaptiveThreshold(self.modifier, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                                   cv2.THRESH_BINARY_INV, self.parameters[0], self.parameters[1])
        elif self.type == 'houghlines':
            filter_applied = cv2.HoughLinesP(self.modifier, self.parameters[0], self.parameters[1] * np.pi / 180,
                                             threshold=self.parameters[2], minLineLength=self.parameters[3],
                                             maxLineGap=self.parameters[4])
        elif self.type == 'canny':
            if self.parameters[2] % 2 == 0:
                self.parameters[2] -= 1
                cv2.setTrackbarPos(self.trackbar_names[2], self.window_name, self.parameters[2])
            filter_applied = cv2.Canny(self.modifier, self.parameters[0], self.parameters[1],
                                       apertureSize=self.parameters[2])
        else:
            print('Invalid threshold type')
            return

        return filter_applied
