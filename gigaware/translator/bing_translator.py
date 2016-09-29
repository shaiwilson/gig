import os
from microsofttranslator import Translator

class BingTranslator:
    def __init__(self):
        client_id = os.environ.get("BING_TRANSLATION_CLIENT_ID", "gigaware123")
        client_secret = os.environ.get("BING_TRANSLATION_SECRET", "Dp3afp41sR/sDsKRK3uWPt2i4WbAKqKB5q6RhCI9a1Q=")

        if not client_id or not client_secret:
            raise Exception("bing translation client id or client secret not found")

        self.translator = Translator(client_id, client_secret)

    def translate(self, untranslated, target_language):
        return self.translator.translate(untranslated, target_language, from_lang='en')

    def translate_all(self, untranslated, target_language):
        return self.translator.translate_array(untranslated, target_language, from_lang='en')