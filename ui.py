import time
from datetime import datetime
import cv2
from models import model2

EYE_POSITION_LEFT = 1
EYE_POSITION_CENTER = 2
EYE_POSITION_RIGHT = 3
SELECTED_CYCLE_THRESHOLD = 20

menus = {
    'L1M1': './menu/L1M1.png',
    'L2M1': './menu/L2M1.png',
    'L2M2': './menu/L2M2.png',
    'L2M3': './menu/L2M3.png',
    'L2MF': './menu/L2MF.png'
}


def run_model(frame):
    return model2(frame)


def focus_left(img):
    cv2.rectangle(img, (40, 161), (385, 456), (0, 255, 0), 15)
    return img


def focus_center(img):
    cv2.rectangle(img, (626, 161), (972, 456), (0, 255, 0), 15)
    return img


def focus_right(img):
    cv2.rectangle(img, (1215, 161), (1560, 456), (0, 255, 0), 15)
    return img


def get_next_menu(current_menu, eye_position):
    # TODO
    next_menu = None

    if current_menu == 'L1M1':
        if eye_position == EYE_POSITION_LEFT:
            next_menu = 'L2M1'
        elif eye_position == EYE_POSITION_CENTER:
            next_menu = 'L2M2'
        elif eye_position == EYE_POSITION_RIGHT:
            next_menu = 'L2M3'

    elif current_menu == 'L2M1':
        if eye_position == EYE_POSITION_LEFT:
            next_menu = 'L1M1'
        elif eye_position == EYE_POSITION_CENTER:
            next_menu = 'L2MF'
        elif eye_position == EYE_POSITION_RIGHT:
            next_menu = 'L1M1'

    elif current_menu == 'L2M2':
        if eye_position == EYE_POSITION_LEFT:
            next_menu = 'L1M1'
        elif eye_position == EYE_POSITION_CENTER:
            next_menu = 'L2MF'
        elif eye_position == EYE_POSITION_RIGHT:
            next_menu = 'L1M1'

    elif current_menu == 'L2M3':
        if eye_position == EYE_POSITION_LEFT:
            next_menu = 'L1M1'
        elif eye_position == EYE_POSITION_CENTER:
            next_menu = 'L2MF'
        elif eye_position == EYE_POSITION_RIGHT:
            next_menu = 'L1M1'
    elif current_menu == 'L2MF':
        if eye_position == EYE_POSITION_LEFT:
            next_menu = 'L1M1'
        elif eye_position == EYE_POSITION_CENTER:
            next_menu = 'L1M1'
        elif eye_position == EYE_POSITION_RIGHT:
            next_menu = 'L1M1'

    return next_menu


def main():

    # initial system config
    current_menu = 'L1M1'
    # i = 0
    # countDict = {'cLeft': 0, 'cRight': 0, 'cCenter': 0, 'cBlinking': 0}
    count_dict = {
        EYE_POSITION_LEFT: 0,
        EYE_POSITION_CENTER: 0,
        EYE_POSITION_RIGHT: 0
    }

    webcam = cv2.VideoCapture(0)

    try:
        while True:
            print(str(menus[current_menu]))
            img = cv2.imread(menus[current_menu], cv2.IMREAD_COLOR)

            _, frame = webcam.read()
            eye_position = run_model(frame)

            if eye_position == EYE_POSITION_LEFT:
                count_dict[EYE_POSITION_LEFT] += 1
                focus_left(img)
                print('LEFT')

            elif eye_position == EYE_POSITION_CENTER:
                count_dict[EYE_POSITION_CENTER] += 1
                focus_center(img)
                print('CENTER')

            elif eye_position == EYE_POSITION_RIGHT:
                count_dict[EYE_POSITION_RIGHT] += 1
                focus_right(img)
                print('RIGHT')

            # elif eye_position == 0:
            #     Blink
                # countDict['cBlinking'] += 1
                # print('Blink')

            else:
                print(eye_position)

            if count_dict[eye_position] >= SELECTED_CYCLE_THRESHOLD:
                next_menu = get_next_menu(current_menu, eye_position)
                if next_menu is not None:
                    current_menu = next_menu
                count_dict = count_dict.fromkeys(count_dict, 0)

            cv2.imshow('Eye On Me', img)
            print(count_dict)
            time.sleep(0.3)

            if cv2.waitKey(1) == 27:
                break
    finally:
        webcam.release()


if __name__ == '__main__':
    main()
