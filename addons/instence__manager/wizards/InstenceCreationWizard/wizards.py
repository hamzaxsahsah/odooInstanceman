from odoo import models, fields, api

class InstanceCreationWizard(models.TransientModel):
    _name = 'instance.creation.wizard'
    _description = 'Instance Creation Wizard'

    sale_order_ids = fields.Many2many('sale.order', string='Sale Orders')
    cpu = fields.Float(string='CPU', required=True)
    ram = fields.Float(string='RAM', required=True)
    disk = fields.Float(string='Disk', required=True)
    tl = fields.Many2one('hr.employee', string="employee")
    name=fields.Char(string="name")
    @api.model
    def default_get(self, fields):
        res = super(InstanceCreationWizard, self).default_get(fields)
        active_ids = self.env.context.get('active_ids')
        res['sale_order_ids'] = active_ids
        return res

    def create_instances(self):
        # Check if CPU, RAM, and Disk values are greater than 0
        if self.cpu <= 0 or self.ram <= 0 or self.disk <= 0:
            raise ValueError("You cannot request instances with zero or negative performance values.")

        # Create instances for each sale order
        created_instances = self.env['kzm.instance.request']
        for sale_order in self.sale_order_ids:
            instance_vals = {
                'cpu': self.cpu,
                'ram': self.ram,
                'disk': self.disk,
                'tl_id': self.tl.id,
                'name' : self.name
                # Add other fields as needed
            }
            instance = self.env['kzm.instance.request'].create(instance_vals)
            created_instances += instance

        # Redirect to the list of created instances
        return {
            'name': 'Created Instances',
            'view_mode': 'tree,form',
            'res_model': 'kzm.instance.request',
            'view_id': False,
            'type': 'ir.actions.act_window',
        }