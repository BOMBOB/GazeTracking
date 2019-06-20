"""
Demonstration of the GazeTracking library.
Check the README.md for complete documentation.
"""

import cv2
from gaze_tracking import GazeTracking

gaze = GazeTracking()
webcam = cv2.VideoCapture(0)
numleft = 0
numright = 0
while True:
    # We get a new frame from the webcam
    ret, frame = webcam.read()
    if ret == False or frame is None:
        continue
    # We send this frame to GazeTracking to analyze it
    gaze.refresh(frame)

    frame = gaze.annotated_frame()
    text = ""

    if gaze.is_blinking():
        text = "Blinking"
    elif gaze.is_right():
        text = "Looking right"
        numright += 1
    elif gaze.is_left():
        text = "Looking left"
        numleft += 1
    elif gaze.is_center():
        text = "Looking center"
    elif gaze.not_found_face():
        text = "Not found face"
        #eye_position = -1

    cv2.putText(frame, text, (90, 60), cv2.FONT_HERSHEY_DUPLEX, 1.6, (147, 58, 31), 2)

    left_pupil = gaze.pupil_left_coords()
    right_pupil = gaze.pupil_right_coords()
    cv2.putText(frame, "Left pupil:  " + str(left_pupil), (90, 130), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)
    cv2.putText(frame, "Right pupil: " + str(right_pupil), (90, 165), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)


    cv2.putText(frame, "numLeft: {} || numRight: {}".format(numleft, numright), (90, 205), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)
    for (x, y) in gaze.shapes:
        cv2.circle(frame, (x, y), 1, (0, 0, 255), -1)
    cv2.imshow("Demo", frame)

    if cv2.waitKey(1) == 27:
        break

