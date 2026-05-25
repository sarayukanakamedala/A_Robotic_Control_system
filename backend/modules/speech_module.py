import speech_recognition as sr

class SpeechRecognizer:

    def __init__(self):
        self.recognizer = sr.Recognizer()

    def listen(self):

        with sr.Microphone() as source:

            print("Speak something...")

            audio = self.recognizer.listen(source)

        try:

            text = self.recognizer.recognize_google(audio)

            return text

        except:

            return None