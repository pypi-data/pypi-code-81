
from ep2_tutors.common import *
import shutil


def idea_checkout(project):
    config = create_config()
    src = local_repo(config, project)
    dst = config.get('Local', 'IdeaEvalDir')

    if os.path.exists(dst):
        for the_file in os.listdir(dst):
            file_path = os.path.join(dst, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path) and the_file != '.idea':
                    shutil.rmtree(file_path)
            except Exception as e:
                print(e)

    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s) and item != '.git' and item != '.idea':
            shutil.copytree(s, d)
        elif os.path.isfile(s):
            shutil.copy2(s, d)