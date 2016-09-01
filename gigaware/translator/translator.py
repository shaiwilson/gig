from flask import Flask

class Translator:
    def __init__(self):
        self.translator = None
        self.target_langauge = None

    def set_translator(self, translator):
        self.translator = translator

    def set_target_translation_language(self, target_language):
        self.target_langauge = target_language

    def translate(self, untranslated):
        if not self.translator or not self.target_langauge:
            raise Exception("Translator has not been initialized")

        return self.translator.translate(untranslated, self.target_langauge)

    def translate_all(self, batched_untranslated):
        if not self.translator or not self.target_langauge:
            raise Exception("Translator has not been initialized")

        return self.translator.translate_all(
            batched_untranslated, 
            self.target_langauge
        )