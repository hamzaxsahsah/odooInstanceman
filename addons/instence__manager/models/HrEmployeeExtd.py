from odoo import models, fields, api
class HrEmployeeInherited(models.Model):
    _inherit = 'hr.employee'

    # Add a One2many field to link with Demande de créations
    instance_ids = fields.One2many('kzm.instance.request', 'tl_id', string='Demande de créations')

    # Add a computed field to calculate the number of instances
    num_instances = fields.Integer(string='Nombre d’instance', compute='_compute_num_instances', store=True)

    @api.depends('instance_ids')
    def _compute_num_instances(self):
        for employee in self:
            employee.num_instances = len(employee.instance_ids)

    def action_view_employee_instances(self):
        action = self.env.ref('instence__manager.action_hr_employee_instances').read()[0]
        action['domain'] = [('tl_id', '=', self.id)]
        return action


