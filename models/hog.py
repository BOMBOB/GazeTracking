import cv2.cv2 as cv2
from gaze_tracking import GazeTracking
gaze = GazeTracking(2)


def analyze(frame):

    gaze.refresh(frame)
    frame = gaze.annotated_frame()
    text = ""
    eye_position = 0

    if gaze.is_blinking():
        text = "Blinking"
        eye_position = 0
    elif gaze.is_right():
        text = "Looking right"
        eye_position = 3
    elif gaze.is_left():
        text = "Looking left"
        eye_position = 1
    elif gaze.is_center():
        text = "Looking center"
        eye_position = 2


    elif gaze.not_found_face():
        text = "Not found face"
        eye_position = -1

    cv2.putText(frame, text, (90, 60), cv2.FONT_HERSHEY_DUPLEX, 1.6, (147, 58, 31), 2)

    left_pupil = gaze.pupil_left_coords()
    right_pupil = gaze.pupil_right_coords()
    cv2.putText(frame, "Left pupil:  " + str(left_pupil), (90, 130), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)
    cv2.putText(frame, "Right pupil: " + str(right_pupil), (90, 165), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)
    cv2.imshow("Demo", frame)
    print(text)

    return eye_position
