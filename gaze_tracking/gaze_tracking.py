from __future__ import division
import os
import cv2
import dlib
from .eye import Eye
from .calibration import Calibration
from .caffe_model import CaffeModel
import numpy as np
 # /Users/Siriphong/Desktop/image-processing/eye-gazing/GazeTracking/gaze_tracking/gaze_tracking.py
face_cascade = cv2.CascadeClassifier()

class GazeTracking(object):
    """
    This class tracks the user's gaze.
    It provides useful information like the position of the eyes
    and pupils and allows to know if the eyes are open or closed
    """

    def __init__(self, choice = 0):
        self.shapes = []
        self.right_list = []
        self.left_list = []
        self.count = 0
        self.numBlink = 0
        self.center_ratio = 0
        self.frame = None
        self.eye_left = None
        self.eye_right = None
        self.calibration = Calibration()
        self.face = None
        self.choice = choice
        # _face_detector is used to detect faces
        self._face_detector = dlib.get_frontal_face_detector()
        self._face_caffe = CaffeModel()
        # _predictor is used to get facial landmarks of a given face
        cwd = os.path.abspath(os.path.dirname(__file__))
        # print('>>path: ', cwd + '/facedetector/haarcascade_frontalface_defaulthaarcascade_frontalface_default.xml')
        model_path = os.path.abspath(os.path.join(cwd, "trained_models/shape_predictor_68_face_landmarks.dat"))
        face_cascade.load(os.path.abspath(os.path.join(cwd, "facedetector/haarcascade_frontalface_default.xml"))
)
        self._predictor = dlib.shape_predictor(model_path)

    @property
    def pupils_located(self):
        """Check that the pupils have been located"""
        try:
            int(self.eye_left.pupil.x)
            int(self.eye_left.pupil.y)
            int(self.eye_right.pupil.x)
            int(self.eye_right.pupil.y)
            return True
        except Exception:
            return False

    def _analyze(self):
        """Detects the face and initialize Eye objects"""
        face = None

        frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
        if self.choice == 0:
            faces = self._face_detector(frame)
            if faces != None and len(faces) > 0:
                # print('>>faces: ', faces)
                face = faces[0]
        elif self.choice == 1:
            face = self._face_caffe._analyze(self.frame)
        elif self.choice == 2:
            cascades = face_cascade.detectMultiScale(frame, 1.3, 5)
            for (x,y,w,h) in cascades:
                face = dlib.rectangle(x,y, x+w, y+h)
        self.face = face
        if face == None:

            self.count += 1
            if self.count > 10:
                self.calibration.reset()
                self.count = 0
                return
            else:
                self.count = 0
                return


        cv2.rectangle(frame, (face.left(), face.top()), (face.right(), face.bottom()), (0, 0, 255), 2)

        try:
            landmarks = self._predictor(frame, face)

            print('>>landmarks: ', landmarks)

            self.eye_left = Eye(frame, landmarks, 0, self.calibration)
            self.eye_right = Eye(frame, landmarks, 1, self.calibration)
            self.shapes = shape_to_np(landmarks)

        except IndexError:
            self.eye_left = None
            self.eye_right = None

    def refresh(self, frame):
        """Refreshes the frame and analyzes it.

        Arguments:
            frame (numpy.ndarray): The frame to analyze
        """
        self.frame = frame
        self._analyze()

    def pupil_left_coords(self):
        """Returns the coordinates of the left pupil"""
        if self.pupils_located:
            x = self.eye_left.origin[0] + self.eye_left.pupil.x
            y = self.eye_left.origin[1] + self.eye_left.pupil.y
            return (x, y)

    def pupil_right_coords(self):
        """Returns the coordinates of the right pupil"""
        if self.pupils_located:
            x = self.eye_right.origin[0] + self.eye_left.pupil.x
            y = self.eye_right.origin[1] + self.eye_left.pupil.y
            return (x, y)

    def horizontal_ratio(self):
        """Returns a number between 0.0 and 1.0 that indicates the
        horizontal direction of the gaze. The extreme right is 0.0,
        the center is 0.5 and the extreme left is 1.0
        """
        if self.pupils_located:
            pupil_left = self.eye_left.pupil.x / (self.eye_left.center[0] * 2 - 10)
            pupil_right = self.eye_right.pupil.x / (self.eye_right.center[0] * 2 - 10)
            ratio = (pupil_left + pupil_right) / 2
            # print('>>horizontal_ratio: ', ratio)
            return ratio

    def vertical_ratio(self):
        """Returns a number between 0.0 and 1.0 that indicates the
        vertical direction of the gaze. The extreme top is 0.0,
        the center is 0.5 and the extreme bottom is 1.0
        """
        if self.pupils_located:
            pupil_left = self.eye_left.pupil.y / (self.eye_left.center[1] * 2 - 10)
            pupil_right = self.eye_right.pupil.y / (self.eye_right.center[1] * 2 - 10)
            return (pupil_left + pupil_right) / 2

    def not_found_face(self):
        if self.face == None:
            return True
    def is_right(self):
        """Returns true if the user is looking to the right"""
        threshold = 0.40
        horizontal = self.horizontal_ratio()
        if len(self.right_list) > 0:
            new_threshold = np.mean(self.right_list);
            if new_threshold < threshold:
                threshold = new_threshold
        if self.pupils_located:
            is_righted = (horizontal <= (threshold+0.03))
            if is_righted:
                self.right_list.append(horizontal)
                if len(self.right_list) > 50:
                    self.right_list = self.right_list[26:50]
                return is_righted

    def is_left(self):
        """Returns true if the user is looking to the left"""
        threshold = 0.75
        horizontal = self.horizontal_ratio()
        if len(self.left_list) > 0:
            new_threshold = np.mean(self.left_list);
            if new_threshold < threshold:
                threshold = new_threshold
        if self.pupils_located:
            is_lefted = (horizontal >= (threshold-0.03))
            if is_lefted:
                self.left_list.append(horizontal)
                if len(self.left_list) > 50:
                    self.left_list = self.left_list[26:50]

                return is_lefted
        #if self.pupils_located:
            # if self.center_ratio != 0:
            #     ratio = 0.38 + ((1 - self.center_ratio) / 2)
            #     print('>>ratio-left: ', ratio)
            #     return self.horizontal_ratio() >= ratio
            #return self.horizontal_ratio() >= 0.75

    def is_center(self):
        """Returns true if the user is looking to the center"""
        if self.pupils_located:
            return self.is_right() is not True and self.is_left() is not True

    def is_blinking(self):
        """Returns true if the user closes his eyes"""
        if self.pupils_located:
            # print(">>Blink: ", self.numBlink)
            blinking_ratio = (self.eye_left.blinking + self.eye_right.blinking) / 2
            print('>>Blink: ', blinking_ratio)
            isBlink = blinking_ratio > 4.5
            # if isBlink:
            #     self.numBlink += 1
            #     if self.numBlink > 3:
            #         self.center_ratio = self.horizontal_ratio()
            #         print('>>self.center_ratio: ', self.center_ratio)
            #         self.numBlink = 0

            return isBlink

    def annotated_frame(self):
        """Returns the main frame with pupils highlighted"""
        frame = self.frame.copy()

        if self.pupils_located:
            color = (0, 255, 0)
            x_left, y_left = self.pupil_left_coords()
            x_right, y_right = self.pupil_right_coords()
            cv2.line(frame, (x_left - 5, y_left), (x_left + 5, y_left), color)
            cv2.line(frame, (x_left, y_left - 5), (x_left, y_left + 5), color)
            cv2.line(frame, (x_right - 5, y_right), (x_right + 5, y_right), color)
            cv2.line(frame, (x_right, y_right - 5), (x_right, y_right + 5), color)
            if len(self.left_list) > 0:
                cv2.putText(frame, "Left List:  " + str(np.min(self.left_list)), (90, 190), cv2.FONT_HERSHEY_DUPLEX, 0.9,
                        (147, 58, 31), 1)
            if len(self.right_list) > 0:
                cv2.putText(frame, "Right List: " + str(np.min(self.right_list)), (90, 225), cv2.FONT_HERSHEY_DUPLEX, 0.9,
                        (147, 58, 31), 1)
            if self.face != None:
                face = self.face

                cv2.rectangle(frame, (face.left(), face.top()), (face.right(), face.bottom()), (0, 0, 255), 2)



        return frame


def shape_to_np(shape, dtype="int"):
    # initialize the list of (x, y)-coordinates
    coords = np.zeros((68, 2), dtype=dtype)

    # loop over the 68 facial landmarks and convert them
    # to a 2-tuple of (x, y)-coordinates
    for i in range(0, 68):
        coords[i] = (shape.part(i).x, shape.part(i).y)

    # return the list of (x, y)-coordinates
    return coords
