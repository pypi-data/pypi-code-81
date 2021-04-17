# This handler copies the file from the source to the target directory,
# substituting any references to project variables with their current values.
#
# For advanced users: Technically, the files get the full Jinja
# treatment, so you can put anything in the file that you can put in a
# Jinja template. But the only variables that will be available are
# project variables.
import os.path
import jinja2
from salal.core.log import log
from salal.core.config import config
from salal.core.dependencies import dependencies
from salal.core.variable_tracker import VariableTracker

class SimpleExpansion:

    #---------------------------------------------------------------------------

    @classmethod
    def get_tags (cls):
        return ['js', 'css', 'py', 'htaccess']

    #---------------------------------------------------------------------------

    @classmethod
    def get_target_extension(cls, source_ext):
        return source_ext
    
    #---------------------------------------------------------------------------

    @classmethod
    def process (cls, tag, source_dir, target_dir, file_stem):
        log.message('TRACE', 'Doing simple expansion')
        env = jinja2.Environment(loader = jinja2.FileSystemLoader(source_dir))
        # In Jinja, template paths aren't file system paths and always use
        # forward slashes regardless of the OS
        template = env.get_template((file_stem + '.' + tag).replace('\\','/'))
        output = template.render({'project': VariableTracker(config.project, success_callback = dependencies.variable_used, failure_callback = dependencies.variable_not_found)})
        with open(os.path.join(target_dir, file_stem + '.' + tag), mode = 'w', encoding = 'utf-8', newline = '\n') as output_fh:
            output_fh.write(output)

    #---------------------------------------------------------------------------

handler = SimpleExpansion
