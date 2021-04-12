from intentBox.segmentation.simple import Segmenter
try:
    import RAKEkeywords
except ImportError:
    RAKEkeywords = None


def segment_keywords(text, lang="en-us"):
    if RAKEkeywords and lang:
        try:
            rake = RAKEkeywords.Rake(lang=lang)
            return rake.extract_keywords(text)
        except:
            pass # lang not supported ?
    return text.split(" ")

