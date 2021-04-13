from pkg_resources import resource_filename

def get_checkpoint_dir():
    return resource_filename(__name__, "")
