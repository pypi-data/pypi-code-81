from tools import *

edp_username = ""
invalid_edp_username = "invalid_username"
edp_password = ""
invalid_edp_password = "invalid_password"
desktop_app_key = ""
invalid_desktop_app_key = "invalid_app_key"

deployed_platform_host = "10.67.4.28:15000"
invalid_deployed_platform_host = "10.67.4.28:00"


def _parse():
    global edp_username, edp_password, desktop_app_key

    desktop_app_key = os.environ.get('DESKTOP_APP_KEY')

    if desktop_app_key is None:
        raise Exception("desktop_app_key is not an env variable, 'DESKTOP_APP_KEY'.")

    edp_password = os.environ.get('EDP_PASSWORD')

    if edp_password is None:
        raise Exception("edp_password is not an env variable, 'EDP_PASSWORD'.")

    edp_username = os.environ.get('EDP_USERNAME')

    if edp_username is None:
        raise Exception("edp_username is not an env variable, 'EDP_USERNAME'.")


_parse()


def prj_config_path():
    from refinitiv.dataplatform import configure

    return os.path.join(os.getcwd(), configure._config_filename)


def user_config_path():
    from refinitiv.dataplatform import configure

    return os.path.join(os.path.expanduser('~'), configure._config_filename)


remove_prj_config = make_remove(prj_config_path)
write_prj_config = make_write(remove_prj_config, prj_config_path)

remove_user_config = make_remove(user_config_path)
write_user_config = make_write(remove_user_config, user_config_path)
