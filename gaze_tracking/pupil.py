import numpy as np
import cv2


class Pupil(object):
    """
    This class detects the iris of an eye and estimates
    the position of the pupil
    """

    def __init__(self, eye_frame, threshold, side=0):
        self.iris_frame = None
        self.threshold = threshold
        self.x = None
        self.y = None
        self.contours = [];
        self.side = side

        self.detect_iris(eye_frame)

    @staticmethod
    def image_processing(eye_frame, threshold):
        """Performs operations on the eye frame to isolate the iris

        Arguments:
            eye_frame (numpy.ndarray): Frame containing an eye and nothing else
            threshold (int): Threshold value used to binarize the eye frame

        Returns:
            A frame with a single element representing the iris
        """
        kernelSharpen = np.array([[0, -1, 0],[-1, 5, -1], [0, -1, 0]])
        kernel = np.ones((3, 3), np.uint8)
        new_frame = cv2.bilateralFilter(eye_frame, 10, 15, 15)
        #new_frame = cv2.filter2D(new_frame, -1, kernelSharpen)

        new_frame = cv2.erode(new_frame, kernel, iterations=3)
        #new_frame = cv2.dirode

        new_frame = cv2.threshold(new_frame, threshold, 255, cv2.THRESH_BINARY)[1]
        # print('>>threshold: ', threshold)

        return new_frame

    def detect_iris(self, eye_frame):
        """Detects the iris and estimates the position of the iris by
        calculating the centroid.

        Arguments:
            eye_frame (numpy.ndarray): Frame containing an eye and nothing else
        """
        self.iris_frame = self.image_processing(eye_frame, self.threshold)

        _, contours, _ = cv2.findContours(self.iris_frame, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        contours = sorted(contours, key=cv2.contourArea)

        try:
            moments = cv2.moments(contours[-2])
            self.x = int(moments['m10'] / moments['m00'])
            self.y = int(moments['m01'] / moments['m00'])
        except (IndexError, ZeroDivisionError):
            pass
        self.drawContours(contours, self.iris_frame)

    def drawContours(self, contours, eye_frame):
        if self.side != 0:
            return;

        # colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
        # ss = ['(blue)', '(green)', '(red)']
        # print('\n==== contours ====')
        # for i in range(len(contours)):
        #     color = colors[i % 3]
        #     s = ss[i % 3]
        #     print('\n' + s + 'Contour#' + str(i) + ' : ' + str(len(contours[i])) + ' points.')
        #
        #     # Print and draw each point storing in the current contour
        #     for j in range(len(contours[i])):
        #         print('  ' + str(j) + '=>', contours[i][j])
        #         center_x, center_y = contours[i][j][0][0], contours[i][j][0][1]
        #         cv2.circle(eye_frame, (center_x, center_y), 6, color, thickness=-1)

        cv2.imshow('>>eye contour: ', eye_frame)


