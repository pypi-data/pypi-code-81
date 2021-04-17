import os
from salal.core.log import log
from salal.core.config import config
from salal.core.handlers import handlers
from salal.core.dependencies import dependencies

class FileProcessing:

    #---------------------------------------------------------------------------

    @classmethod
    def initialize (cls):
        log.message('DEBUG', 'Loading file processing handlers')
        cls.handlers = handlers.load_handlers(config.system['paths']['file_processing_handlers_dir'])
        
    #---------------------------------------------------------------------------

    @classmethod
    def process (cls, source_dir, target_dir, file_relative_path):
        file_stem, ext = os.path.splitext(file_relative_path)
        if file_stem.startswith('.'):
            ext = file_stem
            file_stem = ''
        # strip off the initial '.' in the extension so we just have letters
        ext = ext[1:]
        if ext in cls.handlers:
            tag = ext
        elif 'default' in cls.handlers:
            tag = 'default'
        else:
            log.message('WARN', 'Handling for file type ' + ext + ' is not configured, skipping.')
            return
        target_ext = cls.handlers[tag].get_target_extension(ext)
        source_file = os.path.join(source_dir, file_relative_path)
        target_file = os.path.join(target_dir, file_stem + '.' + target_ext)
        if dependencies.needs_build(target_file, source_file):
            # create the target directory if it doesn't exist
            os.makedirs(os.path.join(target_dir, os.path.dirname(file_relative_path)), exist_ok = True)
            log.message('INFO', source_file)
            dependencies.start_build_tracking(target_file, source_file)
            cls.handlers[tag].process(ext, source_dir, target_dir, file_stem)
            dependencies.stop_build_tracking()

    #---------------------------------------------------------------------------

file_processing = FileProcessing
