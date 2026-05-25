import cv2

from modules.gesture_module import GestureRecognizer
from modules.speech_module import SpeechRecognizer
from modules.translation_module import TranslatorModule
from modules.arm_module import RoboticArm
from services.logger import log_gesture, log_speech, log_translation


gesture_ai = GestureRecognizer()
speech_ai = SpeechRecognizer()
translator = TranslatorModule()
arm = RoboticArm()

cam = cv2.VideoCapture(0)

while True:

    ret, frame = cam.read()

    gesture = gesture_ai.detect(frame)

    if gesture:

        print("Gesture:", gesture)

        log_gesture(gesture)

        arm.move(gesture)


    speech = speech_ai.listen()

    if speech:

        print("Speech:", speech)

        log_speech(speech)

        translated = translator.translate(speech)

        print("Translated:", translated)

        log_translation(speech, translated)


    cv2.imshow("Gesture Camera", frame)

    if cv2.waitKey(1) == ord('q'):
        break


cam.release()
cv2.destroyAllWindows()