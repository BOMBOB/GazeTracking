import cv2
import imutils
from gaze_tracking import GazeTracking
gaze = GazeTracking()


def analyze(frame):
    # We get a new frame from the webcam

    # We send this frame to GazeTracking to analyze it
    frame = zoom(frame, 1)

    gaze.refresh(frame)

    # frame = gaze.annotated_frame()
    text = ""
    eye_position = 0

    if gaze.is_blinking():
        text = "Blinking"
        eye_position = 0
    elif gaze.is_left():
        text = "Looking left"
        eye_position = 1
    elif gaze.is_center():
        text = "Looking center"
        eye_position = 2
    elif gaze.is_right():
        text = "Looking right"
        eye_position = 3

    # cv2.putText(frame, text, (90, 60), cv2.FONT_HERSHEY_DUPLEX, 1.6, (147, 58, 31), 2)

    # left_pupil = gaze.pupil_left_coords()
    # right_pupil = gaze.pupil_right_coords()
    # cv2.putText(frame, "Left pupil:  " + str(left_pupil), (90, 130), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)
    # cv2.putText(frame, "Right pupil: " + str(right_pupil), (90, 165), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)
    # cv2.imshow("Demo", frame)
    # print(text)

    return eye_position


def zoom(cv2Object, zoomSize):
    # Resizes the image/video frame to the specified amount of "zoomSize".
    # A zoomSize of "2", for example, will double the canvas size
    cv2Object = imutils.resize(cv2Object, width=(zoomSize * cv2Object.shape[1]))
    # center is simply half of the height & width (y/2,x/2)
    center = (cv2Object.shape[0] / 2, cv2Object.shape[1] / 2)
    # cropScale represents the top left corner of the cropped frame (y/x)
    cropScale = (center[0] / zoomSize, center[1] / zoomSize)
    # The image/video frame is cropped to the center with a size of the original picture
    # image[y1:y2,x1:x2] is used to iterate and grab a portion of an image
    # (y1,x1) is the top left corner and (y2,x1) is the bottom right corner of new cropped frame.
    cv2Object = cv2Object[cropScale[0]:(center[0] + cropScale[0]), cropScale[1]:(center[1] + cropScale[1])]
    return cv2Object
