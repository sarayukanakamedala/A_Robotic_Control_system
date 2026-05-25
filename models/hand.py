import time
import cv2
import numpy as np
import pickle
import serial
import mediapipe as mp

# ================= SERIAL =================
# CHANGE COM PORT ACCORDING TO YOUR SYSTEM
ser = serial.Serial('COM7', 9600, timeout=1)
time.sleep(2)

last_sent = None   # IMPORTANT: prevents repeated sending

# ================= HAND TRACKING CLASS =================
class mpHands:
    def __init__(self, maxHands=1, modelComplexity=1, tol1=0.5, tol2=0.5):
        self.hands = mp.solutions.hands.Hands(
            static_image_mode=False,
            max_num_hands=maxHands,
            model_complexity=modelComplexity,
            min_detection_confidence=tol1,
            min_tracking_confidence=tol2
        )

    def Marks(self, frame):
        myHands = []
        frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(frameRGB)
        if results.multi_hand_landmarks:
            for handLandMarks in results.multi_hand_landmarks:
                myHand = []
                for lm in handLandMarks.landmark:
                    myHand.append((int(lm.x * width), int(lm.y * height)))
                myHands.append(myHand)
        return myHands

# ================= DISTANCE FUNCTIONS =================
def findDistances(handData):
    distMatrix = np.zeros([len(handData), len(handData)], dtype='float')
    palmSize = ((handData[0][0] - handData[9][0]) ** 2 +
                (handData[0][1] - handData[9][1]) ** 2) ** 0.5

    for r in range(len(handData)):
        for c in range(len(handData)):
            distMatrix[r][c] = (((handData[r][0] - handData[c][0]) ** 2 +
                                 (handData[r][1] - handData[c][1]) ** 2) ** 0.5) / palmSize
    return distMatrix

def findError(gestureMatrix, unknownMatrix, keyPoints):
    error = 0
    for r in keyPoints:
        for c in keyPoints:
            error += abs(gestureMatrix[r][c] - unknownMatrix[r][c])
    return error

def findGesture(unknownGesture, knownGestures, keyPoints, gestNames, tol):
    errors = []
    for i in range(len(gestNames)):
        errors.append(findError(knownGestures[i], unknownGesture, keyPoints))

    minError = min(errors)
    minIndex = errors.index(minError)

    if minError < tol:
        return gestNames[minIndex], minIndex + 1   # RETURN 1–6
    else:
        return "Unknown", 0

# ================= CAMERA SETUP =================
width = 1280
height = 720

cam = cv2.VideoCapture(0)
cam.set(3, width)
cam.set(4, height)

findHands = mpHands()
keyPoints = [0,4,5,9,13,17,8,12,16,20]
tol = 10

# ================= LOAD TRAINED DATA =================
with open("train.pkl", "rb") as f:
    gestNames = pickle.load(f)
    knownGestures = pickle.load(f)

print("✅ Gesture Recognition Started")

# ================= MAIN LOOP =================
while True:
    ret, frame = cam.read()
    frame = cv2.resize(frame, (width, height))

    handData = findHands.Marks(frame)

    if handData:
        unknownGesture = findDistances(handData[0])
        gestureName, gestureNum = findGesture(
            unknownGesture, knownGestures, keyPoints, gestNames, tol
        )

        cv2.putText(frame, gestureName, (50,150),
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (255,0,0), 4)

        if gestureNum != 0:
            cv2.putText(frame, f"Gesture {gestureNum}", (50,220),
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (0,255,0), 4)

            # 🔥 SEND ONLY WHEN CHANGED
            if gestureNum != last_sent:
                ser.write(str(gestureNum).encode())
                print(f"Sent to Arduino: {gestureNum}")
                last_sent = gestureNum
        else:
            if last_sent != 0:
                ser.write(b'6')   # close all
                last_sent = 0

        for pt in keyPoints:
            cv2.circle(frame, handData[0][pt], 15, (255,0,255), 2)

    cv2.imshow("Gesture Control", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# ================= CLEANUP =================
cam.release()
cv2.destroyAllWindows()
ser.close()
