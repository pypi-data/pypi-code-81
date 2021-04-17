# set module language
import wrap_py
from wrap_py import _transl

_transl.set_lang("ru_RU")

# translator for module strings
from wrap_py._transl import translator as _

# translate window title
wrap_py.app.set_title(_(wrap_py.app.get_title()))

# configure wrap_py
wrap_py.make_nice_errors()

# prepare data source
import wds_files_general, wds_files_CoursePythonAdult_1

#first looks in specific sprites
wrap_py.site.sprite_data_sources.append(wds_files_CoursePythonAdult_1.source)
wrap_py.site.sprite_data_sources.append(wds_files_general.source)

wrap_py.site.sprite_data_preload = False

# start in multithreaded mode
wrap_py.init()
