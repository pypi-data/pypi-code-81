
from textblob import TextBlob # Google API, use network
import langid
import pycountry

class LangUtils:

    # Src: https://saimana.com/list-of-country-locale-code/
    locale_country = {'sq': 'AL', 'ar': 'AE', 'be': 'BY', 'bg': 'BG', 'ca': 'ES', 'zh': 'CN', 'hr': 'HR', 'cs': 'CZ', 'da': 'DK', 'nl': 'NL', 'en': 'US', 'et': 'EE', 'fi': 'FI', 'fr': 'FR', 'de': 'DE', 'el': 'GR', 'iw': 'IL', 'hi': 'IN', 'hu': 'HU', 'is': 'IS', 'in': 'ID', 'ga': 'IE', 'it': 'IT', 'ja': 'JP', 'ko': 'KR', 'lv': 'LV', 'lt': 'LT', 'mk': 'MK', 'ms': 'MY', 'mt': 'MT', 'no': 'NO', 'pl': 'PL', 'pt': 'PT', 'ro': 'RO', 'ru': 'RU', 'sr': 'RS', 'sk': 'SK', 'sl': 'SI', 'es': 'ES', 'sv': 'SE', 'th': 'TH', 'tr': 'TR', 'uk': 'UA', 'vi': 'VN'}
    maps_new = {'Viet Nam': 'Vietnam'} # https://www.quora.com/Is-it-Vietnam-or-Viet-Nam,
    def __init__(self):
        pass

    @staticmethod
    def detect_language(text, return_country=False):
        # b = TextBlob(text).detect_language()
        b = langid.classify(text)[0]

        code = LangUtils.locale_country.get(b, None)

        if return_country and code:
            obj = pycountry.countries.get(alpha_2=code)
            if obj.name in LangUtils.maps_new:
                return LangUtils.maps_new.get(obj.name)
            return obj.name
        return code

    @staticmethod
    def get_country_from_text(text):
        return LangUtils.detect_language(text, return_country=True)


if __name__ == '__main__':

    text = 'What is love?'
    print(LangUtils.detect_language(text, return_country=True))

    # for c in pycountry.countries:
    #     print(c.name)