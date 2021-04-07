if 'swissarmykit_conf' not in globals():

    from swissarmykit.lib.core import Singleton, Config

    if Config.is_debug():
        print('DEBUG: load swissarmykit.conf')

    try: from definitions_prod import *
    except Exception as e1:
        from swissarmykit.utils.pathutils import PathUtils

        if PathUtils.set_sys_path():
            try: from definitions_prod import *
            except Exception as e2:
                print('ERROR: from swissarmy.conf import * : load definitions_prod: ', e2)
        else:
            from swissarmykit.templates.definitions_tmp import *
            # print('WARN: temporary load definitions_prod from swissarmykit.templates.definitions.')
            pass
else:
    print('WARN: Already load swissarmykit_conf!')