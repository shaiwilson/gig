from translator import Translator
from bing_translator import BingTranslator

gig_translator = Translator()
gig_translator.set_translator(BingTranslator())
gig_translator.set_target_translation_language('de')