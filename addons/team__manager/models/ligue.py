from odoo import models, fields, api


class ligue(models.Model):
    _name = 'team__manager.ligue'
    _description = 'Football ligue'


    name = fields.Char(string='Date')
    