import os
import wrap_data_source

_PACK_SOURCE_FOLDER = os.path.split(__file__)[0]
_path = os.path.join(_PACK_SOURCE_FOLDER, "sprite_types_gen")
source = wrap_data_source.file_data_source.FileDataSource(_path, sprite_types_subfolder=None, sprite_type_costumes_subfolder=None)