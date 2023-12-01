from odoo import models, fields, api


class goal(models.Model):
    _name = 'team__manager.goal'
    _description = 'Football goal'


    date = fields.Date(string='Date')
    time = fields.Float(string='Time')
    Fixture = fields.One2many('team__manager.fixture','name',string='Fixture')
    Scorrer =  fields.One2many('team__manager.player','name',string='Scorrer')
    Assist = fields.One2many('team__manager.player','name',string='Assist')
    season = fields.Many2one('team__manager.season',string='season')