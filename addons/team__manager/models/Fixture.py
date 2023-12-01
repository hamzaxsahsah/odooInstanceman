from odoo import models, fields, api


class Fixture(models.Model):
    _name = 'team__manager.fixture'
    _description = 'Football Fixture'

    name = fields.Char(string='Fixture Name')
    date = fields.Date(string='Date')
    time = fields.Float(string='Time')
    location = fields.Char(string='Location')
    home_team_id = fields.Many2one('team__manager.team', string='Home Team')
    away_team_id = fields.Many2one('team__manager.team', string='Away Team')
    result = fields.Char(string='Result')
    season = fields.Many2one('team__manager.season',string='season')