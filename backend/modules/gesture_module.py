import cv2
import mediapipe as mp
import numpy as np
import pickle

class GestureRecognizer:

    def __init__(self):

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(
            max_num_hands=1,
            min_detection_confidence=0.6
        )

        with open("../models/gesture_recognition.pkl", "rb") as f:
            self.gesture_names = pickle.load(f)
            self.known_gestures = pickle.load(f)

        self.keypoints = [0,4,5,9,13,17,8,12,16,20]


    def detect(self, frame):

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb)

        if not results.multi_hand_landmarks:
            return None

        return "Gesture Detected"