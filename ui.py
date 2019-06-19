import time
import numpy as np
import cv2.cv2 as cv2
from models import model2 as analyze

EYE_POSITION_LEFT = 1
EYE_POSITION_CENTER = 2
EYE_POSITION_RIGHT = 3
SELECTED_CYCLE_THRESHOLD = 20
RESET_CYCLE_THRESHOLD = 10
SELECT_COLOR = {} # pre-generated when application start

WINDOW_TITLE = "Eye On Me"
BACKGROUND_COLOR = 217
WINDOW_WIDTH = 1440  # 1600
WINDOW_HEIGHT = 900

ICON_WIDTH = 345
ICON_HEIGHT = 295

ICON_LEFT_X1 = 40
ICON_LEFT_Y1 = 161
ICON_LEFT_X2 = ICON_LEFT_X1 + ICON_WIDTH
ICON_LEFT_Y2 = ICON_LEFT_Y1 + ICON_HEIGHT

ICON_RIGHT_X1 = WINDOW_WIDTH - 40 - ICON_WIDTH  # 1215
ICON_RIGHT_Y1 = 161
ICON_RIGHT_X2 = ICON_RIGHT_X1 + ICON_WIDTH
ICON_RIGHT_Y2 = ICON_RIGHT_Y1 + ICON_HEIGHT

ICON_CENTER_X1 = int(WINDOW_WIDTH / 2) - int(ICON_WIDTH / 2)  # 626
ICON_CENTER_Y1 = 161
ICON_CENTER_X2 = ICON_CENTER_X1 + ICON_WIDTH
ICON_CENTER_Y2 = ICON_CENTER_Y1 + ICON_HEIGHT

FONT = cv2.FONT_HERSHEY_COMPLEX
FONT_SCALE = 2
FONT_THICKNESS = 3

menus = {
    'L0': {
        1: {
            'src': './menu/L0L.png',
            'text': 'TOILET'
        },
        3: {
            'src': './menu/L0R.png',
            'text': 'EMERGENCY'
        },
        'children': {
            1: 'L1A',
            # 2: 'L2M2',
            3: 'L1B'
        }
    },
    'L1A': {
        1: {
            'src': './menu/L1AL.png',
            'text': 'NO'
        },
        2: {
            'src': './menu/L1AC.png',
            'text': 'BACK'
        },
        3: {
            'src': './menu/L1AR.png',
            'text': 'YES'
        }
    },
    'L1B': {
        1: {
            'src': './menu/L1BL.png',
            'text': 'NO'
        },
        2: {
            'src': './menu/L1BC.png',
            'text': 'BACK'
        },
        3: {
            'src': './menu/L1BR.png',
            'text': 'HURRY'
        }
    }
}


def run_model(frame):
    return analyze(frame)


def add_icon_left(img, icon):
    if icon is None:
        return None
    alpha_s = icon[:, :, 3] / 255.0
    alpha_l = 1.0 - alpha_s

    for c in range(0, 3):
        img[ICON_LEFT_Y1:ICON_LEFT_Y2, ICON_LEFT_X1:ICON_LEFT_X2, c] = (alpha_s * icon[:, :, c] +
                                                                        alpha_l * img[ICON_LEFT_Y1:ICON_LEFT_Y2,
                                                                                  ICON_LEFT_X1:ICON_LEFT_X2, c])
    return img


def put_text_left(img, text):
    if text is None:
        return None
    text_size = cv2.getTextSize(text, FONT, fontScale=FONT_SCALE, thickness=FONT_THICKNESS)[0]
    text_x = int(ICON_LEFT_X1 + ((ICON_WIDTH - text_size[0]) / 2))
    text_y = int(ICON_LEFT_Y1 + ICON_HEIGHT + text_size[1] + 20)
    cv2.putText(img, text, (text_x, text_y),
                fontFace=FONT,
                fontScale=FONT_SCALE,
                color=(147, 58, 31),
                thickness=FONT_THICKNESS,
                lineType=cv2.LINE_AA)


def focus_left(img, current_percent):
    c = SELECT_COLOR[int(current_percent * 100)]
    cv2.rectangle(img, (ICON_LEFT_X1, ICON_LEFT_Y1), (ICON_LEFT_X2, ICON_LEFT_Y2), c, cv2.FILLED)
    return img


def add_icon_center(img, icon):
    if icon is None:
        return None
    alpha_s = icon[:, :, 3] / 255.0
    alpha_l = 1.0 - alpha_s

    for c in range(0, 3):
        img[ICON_CENTER_Y1:ICON_CENTER_Y2, ICON_CENTER_X1:ICON_CENTER_X2, c] = (alpha_s * icon[:, :, c] +
                                                                        alpha_l * img[ICON_CENTER_Y1:ICON_CENTER_Y2,
                                                                                  ICON_CENTER_X1:ICON_CENTER_X2, c])
    return img


def put_text_center(img, text):
    if text is None:
        return None
    text_size = cv2.getTextSize(text, FONT, fontScale=FONT_SCALE, thickness=FONT_THICKNESS)[0]
    text_x = int(ICON_CENTER_X1 + ((ICON_WIDTH - text_size[0]) / 2))
    text_y = int(ICON_LEFT_Y1 + ICON_HEIGHT + text_size[1] + 20)
    cv2.putText(img, text, (text_x, text_y),
                fontFace=FONT,
                fontScale=FONT_SCALE,
                color=(147, 58, 31),
                thickness=FONT_THICKNESS,
                lineType=cv2.LINE_AA)
    
    
def focus_center(img, current_percent):
    # cv2.rectangle(img, (626, 161), (972, 456), (0, 255, 0), 15)

    c = SELECT_COLOR[int(current_percent * 100)]
    cv2.rectangle(img, (ICON_CENTER_X1, ICON_CENTER_Y1), (ICON_CENTER_X2, ICON_CENTER_Y2), c, cv2.FILLED)

    return img


def add_icon_right(img, icon):
    if icon is None:
        return None
    alpha_s = icon[:, :, 3] / 255.0
    alpha_l = 1.0 - alpha_s

    for c in range(0, 3):
        img[ICON_RIGHT_Y1:ICON_RIGHT_Y2, ICON_RIGHT_X1:ICON_RIGHT_X2, c] = (alpha_s * icon[:, :, c] +
                                                                            alpha_l * img[ICON_RIGHT_Y1:ICON_RIGHT_Y2,
                                                                                      ICON_RIGHT_X1:ICON_RIGHT_X2, c])
    return img


def put_text_right(img, text):
    if text is None:
        return None
    text_size = cv2.getTextSize(text, FONT, fontScale=FONT_SCALE, thickness=FONT_THICKNESS)[0]
    text_x = int(ICON_RIGHT_X1 + ((ICON_WIDTH - text_size[0]) / 2))
    text_y = int(ICON_RIGHT_Y1 + ICON_HEIGHT + text_size[1] + 20)
    cv2.putText(img, text, (text_x, text_y),
                fontFace=FONT,
                fontScale=FONT_SCALE,
                color=(147, 58, 31),
                thickness=FONT_THICKNESS,
                lineType=cv2.LINE_AA)


def focus_right(img, current_percent):
    c = SELECT_COLOR[int(current_percent * 100)]
    cv2.rectangle(img, (ICON_RIGHT_X1, ICON_RIGHT_Y1), (ICON_RIGHT_X2, ICON_RIGHT_Y2), c, cv2.FILLED)
    return img


def get_next_menu(current_menu, eye_position):
    current_menu_item = menus[current_menu]
    if 'children' not in current_menu_item:
        return None
    next_menu = current_menu_item['children'][eye_position]
    return next_menu


# def get_menu_image(menu):
#     return menus[menu]['src']

def get_icon(menu, eye_position):
    if eye_position not in menus[menu]:
        return None
    return menus[menu][eye_position]['src']


def get_text(menu, eye_position):
    if eye_position not in menus[menu]:
        return None
    return menus[menu][eye_position]['text']


def get_left_icon(menu):
    return get_icon(menu, EYE_POSITION_LEFT)


def get_left_text(menu):
    return get_text(menu, EYE_POSITION_LEFT)


def get_center_icon(menu):
    return get_icon(menu, EYE_POSITION_CENTER)


def get_center_text(menu):
    return get_text(menu, EYE_POSITION_CENTER)


def get_right_icon(menu):
    return get_icon(menu, EYE_POSITION_RIGHT)


def get_right_text(menu):
    return get_text(menu, EYE_POSITION_RIGHT)


def has_button_on_position(current_menu, eye_position):
    return current_menu in menus and eye_position in menus[current_menu]


def main():
    # initial system config
    # pre-generate colors
    for i in range(0, 101):
        l_current = min(100, int((90 - 29) * i / 100) + 29)
        hsv = np.uint8([[[60, 148, (l_current / 100) * 255]]])
        bgr = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
        c = (int(bgr[0][0][0]), int(bgr[0][0][1]), int(bgr[0][0][2]))
        SELECT_COLOR[i] = c

    current_menu = 'L0'
    count_dict = {
        EYE_POSITION_LEFT: 0,
        EYE_POSITION_CENTER: 0,
        EYE_POSITION_RIGHT: 0
    }
    img = np.zeros((WINDOW_HEIGHT, WINDOW_WIDTH, 4), dtype=np.uint8)
    img[:, :, :3] = BACKGROUND_COLOR
    cv2.imshow(WINDOW_TITLE, img)

    webcam = cv2.VideoCapture(0)

    try:
        while True:

            img = np.zeros((WINDOW_HEIGHT, WINDOW_WIDTH, 4), dtype=np.uint8)
            img[:, :, :3] = BACKGROUND_COLOR

            _, frame = webcam.read()
            eye_position = run_model(frame)

            if not has_button_on_position(current_menu, eye_position):
                continue

            if count_dict[eye_position] > RESET_CYCLE_THRESHOLD:
                for k in [k for k in count_dict.keys() if k != eye_position]:
                    count_dict[k] = 0

            if eye_position == EYE_POSITION_LEFT:
                count_dict[EYE_POSITION_LEFT] += 1
                focus_left(img, count_dict[EYE_POSITION_LEFT] / SELECTED_CYCLE_THRESHOLD)
                print('LEFT')

            elif eye_position == EYE_POSITION_CENTER:
                count_dict[EYE_POSITION_CENTER] += 1
                focus_center(img, count_dict[EYE_POSITION_CENTER] / SELECTED_CYCLE_THRESHOLD)
                print('CENTER')

            elif eye_position == EYE_POSITION_RIGHT:
                count_dict[EYE_POSITION_RIGHT] += 1
                focus_right(img, count_dict[EYE_POSITION_RIGHT] / SELECTED_CYCLE_THRESHOLD)
                print('RIGHT')

            # elif eye_position == 0:
            #     Blink
            # countDict['cBlinking'] += 1
            # print('Blink')

            else:
                print(eye_position)

            left_icon = cv2.imread(get_left_icon(current_menu), cv2.IMREAD_UNCHANGED)
            add_icon_left(img, left_icon)
            put_text_left(img, get_left_text(current_menu))

            center_icon = cv2.imread(get_center_icon(current_menu), cv2.IMREAD_UNCHANGED)
            add_icon_center(img, center_icon)
            put_text_center(img, get_center_text(current_menu))

            right_icon = cv2.imread(get_right_icon(current_menu), cv2.IMREAD_UNCHANGED)
            add_icon_right(img, right_icon)
            put_text_right(img, get_right_text(current_menu))

            if count_dict[eye_position] >= SELECTED_CYCLE_THRESHOLD:
                next_menu = get_next_menu(current_menu, eye_position)
                if next_menu is not None:
                    current_menu = next_menu
                else:
                    break
                count_dict = count_dict.fromkeys(count_dict, 0)

            cv2.imshow(WINDOW_TITLE, img)
            print(count_dict)
            time.sleep(0.3)

            if cv2.waitKey(1) == 27:
                break
    finally:
        webcam.release()


if __name__ == '__main__':
    main()
