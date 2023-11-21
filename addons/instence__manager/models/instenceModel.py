from datetime import date, datetime

from odoo import models, fields, api, exceptions


class Instence(models.Model):
    _name = 'kzm.instance.request'
    _description = 'Instence Mangement service '
    _inherit = ['mail.thread', 'mail.activity.mixin']

    seq_name = fields.Char(string='Order Reference', required=True, readonly=True)
    name = fields.Char(string='Désignation', required=True, tracking=True)
    adress_ip = fields.Char(string='Adresse IP')
    active = fields.Boolean(string='Actif', default=True)
    cpu = fields.Char(string='CPU')
    ram = fields.Char(string='RAM')
    disk = fields.Char(string='Disk')
    url = fields.Char(string='URL')
    state = fields.Selection([
        ('draft', 'Brouillon'),
        ('submitted', 'Soumise'),
        ('processing', 'En traitement'),
        ('processed', 'Traitée'),
    ], string='Statut', default='draft', tracking=True)
    limit_date = fields.Date(string='Date limite de traitement', tracking=True)
    treat_date = fields.Datetime(string='Date de traitement')
    treat_duration = fields.Float(string='Durée de traitement', compute='calculate_the_duration', store=True)

    partner_id = fields.Many2one('res.partner', string="Client")
    tl_id = fields.Many2one('hr.employee', string="employee")
    tl_user_id = fields.Many2one('res.users', string="user")
    odoo_id = fields.Many2one('odoo.version', string='odooV')
    perimeters_ids = fields.Many2many('perimeter.mang', string="Perimeter")
    perimeters_number = fields.Integer(string='Perimeters', compute='_compute_num_perimeters', store=True)
    _sql_constraints = [
        ('adress_ip', 'UNIQUE (adress_ip)', 'You can not have two same adress ip  !')
    ]

    def action_draft(self):
        for request in self:
            request.write({'state': 'draft'})

    def action_submit(self):
        for request in self:
            request.write({'state': 'submitted'})

    def action_process(self):
        for request in self:
            request.write({'state': 'processing'})

    def action_done(self):
        for request in self:
            mail_template = self.env.ref('instence__manager.email_template_kzm_instance_created')
            mail_template.send_mail(request.id, force_send=True)
            request.write({'state': 'processed', 'treat_date': date.today().strftime("%Y-%m-%d")})

    @api.model
    def create(self, values):
        values['seq_name'] = self.env['ir.sequence'].next_by_code(
            'kzm.instance.request')
        print(values.get('seq_name'))
        if datetime.strptime(str(values['limit_date']), '%Y-%m-%d').date() > date.today():
            # Get the responsible group
            instance_request = super(Instence, self).create(values)
            mail_template = self.env.ref('instence__manager.email_template_kzm_instance_creation')
            mail_template.send_mail(instance_request.id, force_send=True)
            return instance_request

        else:
            raise exceptions.ValidationError("you cannot set a deadline later than today")




    def unlink(self):
        for item in self:
            if item.state == 'draft':
                return super(Instence, item).unlink()
            else:
                raise exceptions.ValidationError("You can only delete instance requests in Draft state")

    def write(self, values):

        if 'limit_date' in values and self.limit_date != values['limit_date']:

            if datetime.strptime(str(values['limit_date']), '%Y-%m-%d').date() > date.today():
                # Get the responsible group
                responsible_group = self.env.ref('instence__manager.group_manager')

                # Create an activity for each user in the responsible group
                for user in responsible_group.users:

                    self.env['mail.activity'].create({
                        'display_name': 'text',
                        'summary': 'text',
                        'date_deadline': values['limit_date'],
                        'user_id': user.id,
                        'res_id': self.id,
                        'res_model_id': self.env['ir.model'].search([('model', '=', 'kzm.instance.request')]).id,
                        'activity_type_id': 6})
                return super(Instence, self).write(values)
            else:
                raise exceptions.ValidationError("you cannot set a deadline later than today")
        else:

            return super(Instence, self).write(values)

    @api.depends('perimeters_ids')
    def _compute_num_perimeters(self):
        for record in self:
            record.perimeters_number = len(record.perimeters_ids)

    @api.depends('limit_date')
    def calculate_the_duration(self):
        for request in self:
            if type(request) == 'datetime.datetime':
                request.treat_duration = (request.limit_date - datetime.today()).days
