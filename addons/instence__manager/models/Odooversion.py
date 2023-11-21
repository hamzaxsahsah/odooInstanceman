from odoo import models, fields, api


class Version(models.Model):
    _name = 'odoo.version'
    _description = 'Odoo Versions management '

    Version = fields.Char(String='Version')



class OdooVersionInherited(models.Model):
    _inherit = 'odoo.version'

    # Add a One2many field to link with Demande de créations
    instance_ids = fields.One2many('kzm.instance.request', 'odoo_id', string='Demande de créations')

    # Add a computed field to calculate the number of instances
    num_instances = fields.Integer(string='Nombre d’instance', compute='_compute_num_instances', store=True)

    @api.depends('instance_ids')
    def _compute_num_instances(self):
        for version in self:
            version.num_instances = len(version.instance_ids)
