import pycowsay
try:
    import finnsinte
except ModuleNotFoundError:
    pass

from sparv import annotator, Document


@annotator("Hej", "cool")
def apa(doc: Document = Document()):
    finnsinte.do()
    pass
