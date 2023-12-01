from odoo import models, fields, api


class Player(models.Model):
    _name = 'team__manager.player'
    _description = 'team__manager.player'

    POSITION_SELECTION = [
    ('goalkeeper', 'Goalkeeper'),
    ('defender_center', 'Center Defender'),
    ('defender_left', 'Left Defender'),
    ('defender_right', 'Right Defender'),
    ('midfielder_defensive', 'Defensive Midfielder'),
    ('midfielder_central', 'Central Midfielder'),
    ('midfielder_left', 'Left Midfielder'),
    ('midfielder_right', 'Right Midfielder'),
    ('forward_center', 'Center Forward'),
    ('forward_left', 'Left Forward'),
    ('forward_right', 'Right Forward'),
]


    name = fields.Char(string='Player Name', required=True)
    position = fields.Selection(POSITION_SELECTION, string='Position')
    team_id = fields.Many2one('team__manager.team', string='Team')
    image =  fields.Binary(string='Picture', attachment=True)