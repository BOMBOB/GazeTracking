import cv2.cv2 as cv2
from models import model1 as analyze

answer = {-1: 0, 0: 0, 1: 12, 2: 0, 3: 9}
count_dict = {-1: 0, 0: 0, 1: 0, 2: 0, 3: 0}

# {-1: 11, 0: 10, 1: 92, 2: 87, 3: 9}

if __name__ == '__main__':
    webcam = cv2.VideoCapture('baseline.mp4')
    try:
        while webcam.isOpened():

            ret, frame = webcam.read()
            if ret:
                eye_position = analyze(frame)
                count_dict[eye_position] += 1
                print(eye_position)
                # cv2.imshow("Evaluation", frame)
                if cv2.waitKey(1) == 27:
                    break
            else:
                break
    finally:
        webcam.release()
        print(count_dict)
