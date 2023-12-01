from odoo import models, fields, api


class Round(models.Model):
    _name = 'team__manager.round'
    _description = 'team__manager.round'
    name = fields.Char(string='Round ', required=True)
    Fixtures_ids = fields.One2many('team__manager.fixture', 'name', string='fixtures')
    season = fields.Many2one('team__manager.season',string='season')