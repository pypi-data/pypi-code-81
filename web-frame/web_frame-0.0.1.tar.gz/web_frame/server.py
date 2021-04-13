# -*- coding: utf-8 -*-
import tornado.ioloop
import tornado.web
import tornado.httpserver
import os
import importlib

import logging

from web_frame.utils.FileUtil import read_yaml

import web_frame.context as context
from web_frame.context import config
# CRITICAL > ERROR > WARNING > INFO > DEBUG > NOTSET
import web_frame.router as router


# 自动导入Handler
def auto_import(path, pkg_name):
    dynamic_handler_names = os.listdir(path)
    for handler_name in dynamic_handler_names:
        full_file = os.path.join(path, handler_name)
        if os.path.isdir(full_file):
            auto_import(os.path.join(path, handler_name), ".".join([pkg_name, handler_name]))
        if os.path.isfile(full_file) and handler_name.endswith(".py"):
            importlib.import_module("{}.{}".format(pkg_name, handler_name.replace(".py", "")))


# 应用实例
class WebServer:
    def __init__(self, cfg, post_init=None):
        config_dict = {}
        if isinstance(cfg, str):
            config_dict = read_yaml(cfg)
        elif isinstance(cfg, dict):
            config_dict.update(cfg)
        elif str(type(cfg)) == '<class \'module\'>':
            for name in dir(cfg):
                if name.startswith("__"):
                    continue
                if name not in config.keys():
                    continue
                val = getattr(cfg, name)
                val_type = str(type(val))
                if val_type in ["<class 'module'>", "<class 'function'>", "<class 'type'>"]:
                    continue
                config_dict[name] = val
        config.update(**config_dict)
        self.context = context
        auto_import(config.handler_path, config.handler_path.replace(config.project_path, '')[1:])
        self.settings = {
            "static_path": config.static_path,
            "template_path": os.path.join(os.path.dirname(__file__), "templates"),
            "cookie_secret": config.cookie_secret,
            "debug": True,
        }
        self.app = tornado.web.Application(
            router.router,
            **self.settings,
            autoreload=True
        )
        self.server = tornado.httpserver.HTTPServer(self.app, max_buffer_size=500 * 1024 * 1024)  # 500M
        self.init_log()
        if post_init:
            if isinstance(post_init, list):
                for func in post_init:
                    func()
            else:
                post_init()

    @staticmethod
    def init_log():
        log_config = {
            "level": config.log_level,
            "format": "%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s"
        }
        if config.log_file:
            fh = logging.FileHandler(os.path.join(config.log_path, "server.log"), encoding="utf-8", mode="a")
            fh.setFormatter(logging.Formatter(log_config["format"]))
            log_config["handlers"] = [fh]
        logging.basicConfig(
            **log_config
        )

    def start(self):
        self.server.listen(config.server_port)
        logging.info(f"start server port : {config.server_port}")
        tornado.ioloop.IOLoop.current().start()
