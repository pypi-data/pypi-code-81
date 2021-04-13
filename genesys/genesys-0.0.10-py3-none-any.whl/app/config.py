import os
SVN_PARENT_PATH = os.getenv("SVN_PARENT_PATH", '/opt/svn/repositories')
SVN_PARENT_URL = os.getenv("SVN_PARENT_URL", "file:////opt/svn/repositories")
FILE_MAP = {
            'shading':'base',
            'concept':'none',
            'modeling':'base',
            'rigging':'base',
            'storyboard':'none',
            'layout':'layout',
            'previz':'layout',
            'animation':'anim',
            'lighting':'lighting',
            'fx':'fx',
            'rendering':'lighting',
            'compositing':'comp',
        }
LOGIN_NAME = os.getenv("LOGIN_NAME", "email")
TEMPLATE_FILES_DIR =os.path.join(os.path.dirname(__file__), 'template_files')