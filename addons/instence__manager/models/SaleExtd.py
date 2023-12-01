from odoo import models, fields


class SaleOrderInherit(models.Model):
    _inherit = "sale.order"

    version_odoo_id = fields.Many2one("odoo.version", string="Odoo Version")

    def action_open_instance_creation_wizard(self):
        return {
            "name": "Create Instances Wizard",
            "view_mode": "form",
            "res_model": "instance.creation.wizard",
            "view_id": self.env.ref(
                "instence__manager.view_instance_creation_wizard_form"
            ).id,
            "type": "ir.actions.act_window",
            "target": "new",
            "context": {"default_sale_order_ids": [(6, 0, self.ids)]},
        }
