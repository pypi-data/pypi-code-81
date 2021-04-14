# -*- coding: utf-8 -*-
# Author: ZKH
# Date：2021/2/27
import os
from config import local_conf_loader


class Config:
    SECRET_KEY = local_conf_loader('SECRET_KEY', '*y=ill@it19yx=s(w7lx&jbk7dm3p+o^&%_v%yeao9@a=o7&c4')
