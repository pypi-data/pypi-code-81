from odoo import api, SUPERUSER_ID

from . import models

XML_ID = "muk_web_theme._assets_primary_variables"
SCSS_URL = "/muk_web_theme/static/src/scss/colors.scss"


def _uninstall_reset_changes(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    env['muk_web_theme.scss_editor'].reset_values(SCSS_URL, XML_ID)
