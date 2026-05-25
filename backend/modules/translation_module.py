from googletrans import Translator

class TranslatorModule:

    def __init__(self):
        self.translator = Translator()

    def translate(self, text, target="te"):

        result = self.translator.translate(text, dest=target)

        return result.text