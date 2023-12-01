from odoo import models, fields, api


class season(models.Model):
    _name = 'team__manager.season'
    _description = 'team__manager season'
    
    start = fields.Date()
    end = fields.Date()
    

   