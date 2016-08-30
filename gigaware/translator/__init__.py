from translator import Translator
from bing_translator import BingTranslator

gig_translator = Translator()
gig_translator.set_translator(BingTranslator())
gig_translator.set_target_translation_language('de')

def translate(untranslated):
    return gig_translator.translate(untranslated)

def translate_all(batched_untranslated):
    return gig_translator.translate_all(batched_untranslated)

def test_translate(test):
    return gig_translator.test_translate(test)