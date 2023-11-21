from odoo import models, fields




class Perimetre(models.Model):
    _name = 'perimeter.mang'
    _description = 'Perimetre management '

    name = fields.Char(String='name')