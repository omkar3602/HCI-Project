import mediapipe as mp
import cv2
from constants import s_width, s_height

mediapipeHands = mp.solutions.hands
hands = mediapipeHands.Hands()
# mediapipeDraw = mp.solutions.drawing_utils

def get_gestures(cap):
    success, img = cap.read()
    img = cv2.flip(img, 1)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    results = hands.process(img)


    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            for id, lm in enumerate(handLms.landmark):
                h, w, c = img.shape
                if id == 0:
                    x = []
                    y = []
                x.append(int((lm.x) * w))
                y.append(int((1 - lm.y) * h))

                #Gestos
                if len(y) > 20:
                    if (x[0] > x[3] > x[4]) and not(y[20] > y[17]):
                        return 'left'
                    elif not(x[0] > x[3] > x[4]) and (y[20] > y[17]):
                        return 'right'
                    elif (x[0] > x[3] > x[4]) and (y[20] > y[17]):
                        return 'rotate'
                    # TODO (down gesture) elif:
                        # return 'down'


            # mediapipeDraw.draw_landmarks(img, handLms, mediapipeHands.HAND_CONNECTIONS)
    else:
        return None