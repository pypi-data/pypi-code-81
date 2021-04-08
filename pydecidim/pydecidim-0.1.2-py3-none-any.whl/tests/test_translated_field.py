import unittest

from pydecidim.model.translated_field import TranslatedField


class TranslatedFieldTest(unittest.TestCase):
    def test_get_locales(self):
        translations = {'ca': "Bon dia", 'es': "Buenos días", 'en': "Good Morning"}
        translated_field : TranslatedField = TranslatedField(translations)
        locales = translated_field.locales
        self.assertEqual(locales, ("ca", "es", "en"))

    def test_get_translations(self):
        translations = {'ca': "Bon dia", 'es': "Buenos días", 'en': "Good Morning"}
        translated_field : TranslatedField = TranslatedField(translations)
        translations_retrieved = translated_field.get_translations(['ca', 'es', 'en'])
        self.assertEqual(translations, translations_retrieved)

    def test_get_translation(self):
        translations = {'ca': "Bon dia", 'es': "Buenos días", 'en': "Good Morning"}
        translated_field: TranslatedField = TranslatedField(translations)
        translation_ca = translated_field.get_translation('ca')
        translation_es = translated_field.get_translation('es')
        translation_en = translated_field.get_translation('en')
        translation_unknown = translated_field.get_translation('unknown')

        self.assertEqual(translation_ca, "Bon dia")
        self.assertEqual(translation_es, "Buenos días")
        self.assertEqual(translation_en, "Good Morning")
        self.assertIsNone(translation_unknown)




if __name__ == '__main__':
    unittest.main()
