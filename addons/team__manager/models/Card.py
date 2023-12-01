from odoo import models, fields, api


class card(models.Model):
    _name = 'team__manager.card'
    _description = 'Football cards'

    type = fields.Char(string='cardTyper')
    date = fields.Date(string='Date')
    time = fields.Float(string='Time')
    Fixture = fields.One2many('team__manager.fixture','name',string='Fixture')
    season = fields.Many2one('team__manager.season',string='season')