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
        hand_landmarks = results.multi_hand_landmarks[0]

        thumb_tip = hand_landmarks.landmark[mediapipeHands.HandLandmark.THUMB_TIP]
        thumb_mcp = hand_landmarks.landmark[mediapipeHands.HandLandmark.THUMB_MCP]
        wrist = hand_landmarks.landmark[mediapipeHands.HandLandmark.WRIST]

        if thumb_tip.y < thumb_mcp.y:
            fingers_up = [
                hand_landmarks.landmark[mediapipeHands.HandLandmark.INDEX_FINGER_TIP].y <
                hand_landmarks.landmark[mediapipeHands.HandLandmark.INDEX_FINGER_DIP].y,
                hand_landmarks.landmark[mediapipeHands.HandLandmark.MIDDLE_FINGER_TIP].y <
                hand_landmarks.landmark[mediapipeHands.HandLandmark.MIDDLE_FINGER_DIP].y,
                hand_landmarks.landmark[mediapipeHands.HandLandmark.RING_FINGER_TIP].y <
                hand_landmarks.landmark[mediapipeHands.HandLandmark.RING_FINGER_DIP].y,
                hand_landmarks.landmark[mediapipeHands.HandLandmark.PINKY_TIP].y <
                hand_landmarks.landmark[mediapipeHands.HandLandmark.PINKY_DIP].y,
            ]
            if all(fingers_up):
                return "rotate"
        if thumb_tip.y > thumb_mcp.y:
            fingers_down = [
                hand_landmarks.landmark[mediapipeHands.HandLandmark.INDEX_FINGER_TIP].y >
                hand_landmarks.landmark[mediapipeHands.HandLandmark.INDEX_FINGER_DIP].y,
                hand_landmarks.landmark[mediapipeHands.HandLandmark.MIDDLE_FINGER_TIP].y >
                hand_landmarks.landmark[mediapipeHands.HandLandmark.MIDDLE_FINGER_DIP].y,
                hand_landmarks.landmark[mediapipeHands.HandLandmark.RING_FINGER_TIP].y >
                hand_landmarks.landmark[mediapipeHands.HandLandmark.RING_FINGER_DIP].y,
                hand_landmarks.landmark[mediapipeHands.HandLandmark.PINKY_TIP].y >
                hand_landmarks.landmark[mediapipeHands.HandLandmark.PINKY_DIP].y,
            ]
            if all(fingers_down):
                return "down"
        if thumb_tip.x < thumb_mcp.x:
            return "left"
        elif thumb_tip.x > thumb_mcp.x:
            return "right"
        
            
            # mediapipeDraw.draw_landmarks(img, handLms, mediapipeHands.HAND_CONNECTIONS)
    else:
        return None