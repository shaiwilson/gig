from translator import Translator
from bing_translator import BingTranslator

import redis
import os

REDIS_HOST = os.environ.get("REDIS_HOST", "localhost")
REDIS_PORT = os.environ.get("REDIS_PORT", "6379")

gig_redis = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=0)

TARGET_TRANSLATION_LANG = 'de'

gig_translator = Translator()
gig_translator.set_translator(BingTranslator())
gig_translator.set_target_translation_language(TARGET_TRANSLATION_LANG)


def build_localizable_key(untranslated, target_translation_lang):
    return 'giglocalizable%%%' + untranslated + '%%%' + target_translation_lang


def translate(untranslated):
    key = build_localizable_key(untranslated, TARGET_TRANSLATION_LANG)

    # If redis contains the localized string in the target language, return it.
    try:
        localized = gig_redis.get(key)
    except redis.exceptions.ConnectionError:
        # No redis connection? Return the untranslated string.
        return untranslated

    if localized:
        return localized.decode("utf-8")

    # Otherwise, ask bing for the translation, and set the returned translation
    # in redis.
    localized = gig_translator.translate(untranslated)
    gig_redis.set(key, localized)
    return localized.decode("utf-8")
