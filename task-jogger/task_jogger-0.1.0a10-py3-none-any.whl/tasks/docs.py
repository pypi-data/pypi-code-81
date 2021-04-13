import os

from jogger.utils.input import JOG_FILE_NAME, find_config_file

from .base import Task, TaskError

try:
    import sphinx  # noqa
    HAS_SPHINX = True
except ImportError:
    HAS_SPHINX = False


class DocsTask(Task):
    
    help = (
        'Build the project documentation using Sphinx.'
    )
    
    def add_arguments(self, parser):
        
        parser.add_argument(
            '-f', '--full',
            action='store_true',
            dest='full',
            help=(
                'Remove previously built documentation before rebuilding all '
                'pages from scratch.'
            )
        )
        
        parser.add_argument(
            '-l', '--link',
            action='store_true',
            dest='link_only',
            help='Output the link to previously built documentation and exit.'
        )
    
    def handle(self, **options):
        
        if not HAS_SPHINX:
            raise TaskError('Sphinx not detected.')
        
        # Get the project directory by locating the task file (jog.py). Assume
        # a "docs" directory under that.
        project_dir = os.path.dirname(find_config_file(JOG_FILE_NAME))
        docs_dir = os.path.join(project_dir, 'docs')
        
        if not os.path.exists(docs_dir):
            raise TaskError(f'Documentation directory not found at {docs_dir}.')
        
        if options['link_only']:
            show_link = True
        else:
            command = [f'cd {docs_dir}']
            if options['full']:
                command.append('make clean')
            
            command.append('make html')
            
            result = self.cli(' && '.join(command))
            show_link = result.returncode == 0
            self.stdout.write('')  # blank line
        
        if show_link:
            index_path = os.path.join(docs_dir, '_build', 'html', 'index.html')
            if os.path.exists(index_path):
                self.stdout.write(f'Generated documentation index: {index_path}')
                
                index_url = f'file://{index_path}'
                path_swap = self.settings.get('path_swap', None)
                if path_swap:
                    if ';' not in path_swap:
                        raise TaskError('Invalid format for path_swap setting.')
                    
                    old_path, new_path = path_swap.split(';')
                    index_url = index_url.replace(old_path, new_path)
                
                self.stdout.write(f'View the documentation at: {self.styler.label(index_url)}')
            else:
                self.stdout.write(f'Generated documentation index not found, expected: {index_path}', style='warning')
