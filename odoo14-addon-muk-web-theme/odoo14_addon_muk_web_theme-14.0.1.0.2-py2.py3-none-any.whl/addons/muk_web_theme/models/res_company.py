from odoo import models, fields


class ResCompany(models.Model):
    
    _inherit = 'res.company'
    
    #----------------------------------------------------------
    # Database
    #----------------------------------------------------------
    
    background_image = fields.Binary(
        string="Apps Menu Background Image",
        attachment=True
    )
    
    background_blend_mode = fields.Selection(
        selection=[
            ('normal', 'Normal'),
            ('multiply', 'Multiply'),
            ('screen', 'Screen'),
            ('overlay', 'Overlay'),
            ('hard-light', 'Hard-light'),
            ('darken', 'Darken'),
            ('lighten', 'Lighten'),
            ('color-dodge', 'Color-dodge'),
            ('color-burn', 'Color-burn'),
            ('hard-light', 'Hard-light'),
            ('difference', 'Difference'),
            ('exclusion', 'Exclusion'),
            ('hue', 'Hue'),
            ('saturation', 'Saturation'),
            ('color', 'Color'),
            ('luminosity', 'Luminosity'),
        ], 
        string="Apps Menu Background Blend Mode",
        default='normal'
    )
    
    default_sidebar_preference = fields.Selection(
        selection=[
            ('invisible', 'Invisible'),
            ('small', 'Small'),
            ('large', 'Large')
        ], 
        string="Sidebar Type",
        default='small'
    )
    
    default_chatter_preference = fields.Selection(
        selection=[
            ('normal', 'Normal'),
            ('sided', 'Sided'),
        ], 
        string="Chatter Position", 
        default='sided'
    )
