import os, sys

TRANSL_DOMAIN = "wrap_py"
PACK_SOURCE_FOLDER = os.path.split(__file__)[0]
TRANSLATIONS_FOLDER = os.path.join(PACK_SOURCE_FOLDER, "transl", "compiled")

RESOURCE_FOLDER = os.path.join(PACK_SOURCE_FOLDER, "res")
ICON_FILE = os.path.join(RESOURCE_FOLDER, "icon.png")