from odoo import models
from odoo.http import request


class IrHttp(models.AbstractModel):
    
    _inherit = 'ir.http'

    def session_info(self):
        result = super(IrHttp, self).session_info()
        params = request.env['ir.config_parameter'].sudo()
        blend_mode = params.get_param('muk_web_theme.background_blend_mode')
        result.update(muk_web_theme_background_blend_mode=blend_mode or 'normal')
        return result
