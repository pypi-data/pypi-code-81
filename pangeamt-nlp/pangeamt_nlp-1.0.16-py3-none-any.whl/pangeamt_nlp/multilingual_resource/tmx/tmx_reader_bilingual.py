from pangeamt_nlp.locale.locale import Locale
from pangeamt_nlp.multilingual_resource.tmx.tmx import Tmx
import warnings
class TmxReaderBilingualText:
    def __init__(self, src_lang, tgt_lang):
        self._src_lang = src_lang

        self._tgt_lang = tgt_lang

        self._tmx_src_locale = None
        self._tmx_tgt_locale = None

    def read(self, segs_by_locale):
        src_locales = [locale for locale in segs_by_locale if any(src_lang in Locale.to_lang(locale) for src_lang in [self._src_lang, self._src_lang.upper()])]
        if len(src_locales) == 0:
            warnings.warn(f"TmxExtractorBilingualText. No src_locales for this segment")
        elif len(src_locales) > 1:
            #raise ValueError(f"TmxExtractorBilingualText. More than one language for {self._src_lang}: {''.join(src_locales)}")
            warnings.warn(f"TmxExtractorBilingualText. More than one language for {self._src_lang}: {''.join(src_locales)}")
        else:
            self._tmx_src_locale = src_locales[0]
        
        tgt_locales = [locale for locale in segs_by_locale if any(tgt_lang in Locale.to_lang(locale) for tgt_lang in [self._tgt_lang, self._tgt_lang.upper()])]
        if len(tgt_locales) == 0:
            warnings.warn(f"TmxExtractorBilingualText. No tgt_locales for this segment")
        elif len(tgt_locales) > 1:
            #raise ValueError(f"TmxExtractorBilingualText. More than one language for {self._tgt_lang}: {''.join(tgt_locales)}")
            warnings.warn(f"TmxExtractorBilingualText. More than one language for {self._tgt_lang}: {''.join(tgt_locales)}")
        else:
            self._tmx_tgt_locale = tgt_locales[0]

        try:
            src = segs_by_locale[self._tmx_src_locale]
        except KeyError:
            #raise ValueError(f"TmxExtractorBilingualText. {self._src_lang} is mapped to {self._tmx_src_locale} and no segment was find for that locale")
            src = ''
            warnings.warn(f'TmxExtractorBilingualText. {self._src_lang} is mapped to {self._tmx_src_locale} and no segment was found for that locale')

        try:
            tgt = segs_by_locale[self._tmx_tgt_locale]
        except KeyError:
            #raise ValueError(f"TmxExtractorBilingualText. {self._tgt_lang} is mapped to {self._tmx_tgt_locale} and no segment was find for that locale")
            tgt = ''
            warnings.warn(f'TmxExtractorBilingualText. {self._tgt_lang} is mapped to {self._tmx_tgt_locale} and no segment was found for that locale')
        if src == '' or tgt == '':
            return '[[[@@@MISSING_TRANSLATION@@@]]]', '[[[@@@MISSING_TRANSLATION@@@]]]'
        else:
            return Tmx.seg_to_text(src), Tmx.seg_to_text(tgt)

