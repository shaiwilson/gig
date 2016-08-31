from translator import Translator
from bing_translator import BingTranslator
import redis

gig_redis = redis.StrictRedis(host='localhost', port=6379, db=0)

TARGET_TRANSLATION_LANG = 'de'

gig_translator = Translator()
gig_translator.set_translator(BingTranslator())
gig_translator.set_target_translation_language(TARGET_TRANSLATION_LANG)


def build_localizable_key(untranslated, target_translation_lang):
    return 'giglocalizable%%%' + untranslated + '%%%' + target_translation_lang


def translate(untranslated):
    key = build_localizable_key(untranslated, TARGET_TRANSLATION_LANG)

    # If redis contains the localized string in the target language, return it.
    localized = gig_redis.get(key)
    if localized:
        return localized.decode("utf-8")

    # Otherwise, ask bing for the translation, and set the returned translation
    # in redis.
    localized = gig_translator.translate(untranslated)
    gig_redis.set(key, localized)
    return localized.decode("utf-8")
