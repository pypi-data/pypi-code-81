import sys, os, configparser

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame

_ = lambda x: x


def _log_action(info, warnings, prefix, text, do_warning=False):
    text = prefix + " " + text
    if info is not None:
        info.append(text)
    if do_warning and warnings is not None:
        warnings.append(text)


class Costume_loader():
    @staticmethod
    def load_config(cfg_path, data, infos, warnings, prefix):
        # check existance
        if not os.path.isfile(cfg_path):
            _log_action(infos, warnings, prefix, _("No costume config found."))
            return False

        # try to load
        try:
            cfg = configparser.ConfigParser()
            cfg.read(cfg_path)
        except:
            exc_txt = str(sys.exc_info()[1])
            _log_action(infos, warnings, prefix, _("Config loading error") + ": " + exc_txt, True)
            return False

        _log_action(infos, warnings, prefix, _("Costume config found."))

        # read base config
        try:
            data['posx'] = cfg.getint("IMAGE", "posx", fallback=None)
            data['posy'] = cfg.getint("IMAGE", "posy", fallback=None)
            data['angle'] = cfg.getint("IMAGE", "angle", fallback=90)

        except:
            exc_txt = str(sys.exc_info()[1])
            _log_action(infos, warnings, prefix, _("Config reading error") + ": " + exc_txt, True)
            return False

        # read optional 'process' part
        if not cfg.has_section("PROCESS"):
            return True

        try:
            process = {}
            data['process'] = process
            process['width'] = cfg.getint("PROCESS", "width", fallback=None)
            process['height'] = cfg.getint("PROCESS", "height", fallback=None)
            process['remove_color'] = cfg.getboolean("PROCESS", "remove_color", fallback=False)
        except:
            exc_txt = str(sys.exc_info()[1])
            _log_action(infos, warnings, prefix, _("Config reading error") + ": " + exc_txt, True)
            return False

        # read optional remove color details
        if not process['remove_color']:
            return True

        try:
            # if remove_color is True then r, g, b must be defined
            if not cfg.has_option('PROCESS', 'remove_color_r') or \
                    not cfg.has_option('PROCESS', 'remove_color_g') or \
                    not cfg.has_option('PROCESS', 'remove_color_b'):
                raise Exception(_("Remove color parameters not found"))

            r = cfg.getint("PROCESS", "remove_color_r")
            if not 0 <= r <= 255: raise Exception(_("Remove color R is invalid") + ":" + str(r))

            g = cfg.getint("PROCESS", "remove_color_g")
            if not 0 <= g <= 255: raise Exception(_("Remove color G is invalid") + ":" + str(g))

            b = cfg.getint("PROCESS", "remove_color_b")
            if not 0 <= b <= 255: raise Exception(_("Remove color B is invalid") + ":" + str(b))

            process['remove_color_rgb'] = [r, g, b]

            thr = cfg.getint("PROCESS", "remove_color_thr", fallback=1)
            if not 1 <= thr <= 255: raise Exception(_("Color threshold is invalid") + ":" + str(thr))
            process['remove_color_thr'] = thr


        except:
            exc_txt = str(sys.exc_info()[1])
            _log_action(infos, warnings, prefix, _("Config reading error") + ": " + exc_txt, True)
            return False

        return True

    @staticmethod
    def default_config(data):
        data['posx'] = None
        data['posy'] = None
        data['angle'] = 90

    @staticmethod
    def load_data(path, infos=None, warnings=None, prefix=""):

        res = {}

        _log_action(infos, warnings, prefix, _("loading") + " " + path)

        # check path exists
        if not os.path.exists(path):
            _log_action(infos, warnings, prefix, _("Costume image file not found") + ": " + path, True)
            return False

        # check path is file
        if not os.path.isfile(path):
            _log_action(infos, warnings, prefix, _("Costume image must be a file. Not a directory."), True)
            return False

        # load image
        try:
            image = pygame.image.load(path)
            # image.set_alpha(255)
        except:

            exc_txt = str(sys.exc_info()[1])
            _log_action(infos, warnings, prefix, exc_txt, True)

            return False

        # extract name
        head, tail = os.path.split(path)
        name, ext = os.path.splitext(tail)

        res['image_file'] = path
        res['name'] = name
        res['image'] = image

        # load config
        head, ext = os.path.splitext(path)
        cfg_path = head + ".ini"
        config_data = {}
        if Costume_loader.load_config(cfg_path, config_data, infos, warnings, prefix):
            res['config_file'] = cfg_path
        else:
            res['config_file'] = None
            config_data = {}
            Costume_loader.default_config(config_data)

        # copy data to result
        for i in config_data:
            res[i] = config_data[i]

        return res
