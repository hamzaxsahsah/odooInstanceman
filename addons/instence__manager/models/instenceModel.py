from datetime import date, datetime
import base64
from odoo import models, fields, api, exceptions
import xlwt
from io import BytesIO


class Instence(models.Model):
    _name = "kzm.instance.request"
    _description = "Instence Mangement service "
    _inherit = ["mail.thread", "mail.activity.mixin"]

    seq_name = fields.Char(string="Order Reference", required=True, readonly=True)
    name = fields.Char(string="Désignation", required=True, tracking=True)
    adress_ip = fields.Char(string="Adresse IP")
    active = fields.Boolean(string="Actif", default=True)
    cpu = fields.Char(string="CPU")
    ram = fields.Char(string="RAM")
    disk = fields.Char(string="Disk")
    url = fields.Char(string="URL")
    state = fields.Selection(
        [
            ("draft", "Brouillon"),
            ("submitted", "Soumise"),
            ("processing", "En traitement"),
            ("processed", "Traitée"),
        ],
        string="Statut",
        default="draft",
        tracking=True,
    )
    limit_date = fields.Date(string="Date limite de traitement", tracking=True)
    treat_date = fields.Datetime(string="Date de traitement")
    treat_duration = fields.Float(
        string="Durée de traitement", compute="calculate_the_duration", store=True
    )

    partner_id = fields.Many2one("res.partner", string="Client")
    tl_id = fields.Many2one("hr.employee", string="employee")
    tl_user_id = fields.Many2one("res.users", string="user")
    odoo_id = fields.Many2one("odoo.version", string="odooV")
    perimeters_ids = fields.Many2many("perimeter.mang", string="Perimeter")
    perimeters_number = fields.Integer(
        string="Perimeters", compute="_compute_num_perimeters", store=True
    )
    _sql_constraints = [
        ("adress_ip", "UNIQUE (adress_ip)", "You can not have two same adress ip  !")
    ]

    def action_draft(self):
        """
        Set state to draft. This is a no - op for requests that don't have a state
        """
        # Write the state of the current request to the server.
        for request in self:
            request.write({"state": "draft"})

    def action_submit(self):
        """
        Submit the request to the API. This is a no - op for requests that don't require a submit
        """
        # Write the state of the request to the server.
        for request in self:
            request.write({"state": "submitted"})

    def action_process(self):
        """
        Called when the user presses the process button. This is a no - op for this action but can be used to change the state
        """
        # Write state processing to the server
        for request in self:
            request.write({"state": "processing"})

    def action_done(self):
        """
        Send email to KZM when instance is processed. We don't care about this in case of failure
        """
        # Send the email to the instance created mails
        for request in self:
            mail_template = self.env.ref(
                "instence__manager.email_template_kzm_instance_created"
            )
            mail_template.send_mail(request.id, force_send=True)
            request.write(
                {"state": "processed", "treat_date": date.today().strftime("%Y-%m-%d")}
            )

    @api.model
    def create(self, values):
        """
        Create and send an email to KZM if deadline is later than today. This is to avoid creating instances that are in the future

        @param values - dictionary of key value pairs

        @return Instance request that was created and sent to KZM if deadline is later than today. Otherwise raise
        """
        values["seq_name"] = self.env["ir.sequence"].next_by_code(
            "kzm.instance.request"
        )
        print(values.get("seq_name"))
        # Create a new instance request.
        if (
            datetime.strptime(str(values["limit_date"]), "%Y-%m-%d").date()
            > date.today()
        ):
            # Get the responsible group
            instance_request = super(Instence, self).create(values)
            mail_template = self.env.ref(
                "instence__manager.email_template_kzm_instance_creation"
            )
            mail_template.send_mail(instance_request.id, force_send=True)
            return instance_request

        else:
            raise exceptions.ValidationError(
                "you cannot set a deadline later than today"
            )

    def unlink(self):
        """
        Unlink an Instence from the database. This is an override of the parent method to check if the request is in draft state before unlinking


        @return True if successful False
        """
        # Delete instance requests in Draft state
        for item in self:
            # Delete instance requests in Draft state
            if item.state == "draft":
                return super(Instence, item).unlink()
            else:
                raise exceptions.ValidationError(
                    "You can only delete instance requests in Draft state"
                )

    def write(self, values):
        # This method is called by the controller when the limit_date is set to the current date.
        if "limit_date" in values and self.limit_date != values["limit_date"]:
            # This method will write the instence to the instence.
            if (
                datetime.strptime(str(values["limit_date"]), "%Y-%m-%d").date()
                > date.today()
            ):
                # Get the responsible group
                responsible_group = self.env.ref("instence__manager.group_manager")

                # Create an activity for each user in the responsible group
                # Create activity for each user in responsible_group. users
                for user in responsible_group.users:
                    self.env["mail.activity"].create(
                        {
                            "display_name": "text",
                            "summary": "text",
                            "date_deadline": values["limit_date"],
                            "user_id": user.id,
                            "res_id": self.id,
                            "res_model_id": self.env["ir.model"]
                            .search([("model", "=", "kzm.instance.request")])
                            .id,
                            "activity_type_id": 6,
                        }
                    )
                return super(Instence, self).write(values)
            else:
                raise exceptions.ValidationError(
                    "you cannot set a deadline later than today"
                )
        else:
            return super(Instence, self).write(values)

    @api.depends("perimeters_ids")
    def _compute_num_perimeters(self):
        """
        Compute and set perimeters_number for each record. This is used to compute the number of perimeters
        """
        # Set the number of perimeters of each record
        for record in self:
            record.perimeters_number = len(record.perimeters_ids)

    @api.depends("limit_date")
    def calculate_the_duration(self):
        """
        Calculate the duration of the request based on the limit_date. This is used to decide how long we want to treat
        """
        # Set the treat duration of the request.
        for request in self:
            # If request is datetime. datetime then the request will be treated as duration.
            if type(request) == "datetime.datetime":
                request.treat_duration = (request.limit_date - datetime.today()).days

    def export_to_excel(self):
        workbook = xlwt.Workbook()
        worksheet = workbook.add_sheet("Instance Requests")

        # Add headers
        headers = [
            "Reference",
            "Designation",
            "IP Address",
            "Active",
            "CPU",
            "RAM",
            "Disk",
            "URL",
            "Status",
            "Limit Date",
            "Treatment Date",
            "Treatment Duration",
            "Client",
            "Employee",
            "User",
            "Odoo Version",
            "Perimeter IDs",
            "Perimeters Number",
        ]
        for col_num, header in enumerate(headers):
            worksheet.write(0, col_num, header)

        # Add data
        for row_num, instance in enumerate(self):
            worksheet.write(row_num + 1, 0, instance.seq_name)
            worksheet.write(row_num + 1, 1, instance.name)
            worksheet.write(row_num + 1, 2, instance.adress_ip)
            worksheet.write(row_num + 1, 3, instance.active)
            worksheet.write(row_num + 1, 4, instance.cpu)
            worksheet.write(row_num + 1, 5, instance.ram)
            worksheet.write(row_num + 1, 6, instance.disk)
            worksheet.write(row_num + 1, 7, instance.url)
            worksheet.write(row_num + 1, 8, instance.state)
            worksheet.write(row_num + 1, 9, instance.limit_date)
            worksheet.write(row_num + 1, 10, instance.treat_date)
            worksheet.write(row_num + 1, 11, instance.treat_duration)
            worksheet.write(row_num + 1, 12, instance.partner_id.name)
            worksheet.write(row_num + 1, 13, instance.tl_id.name)
            worksheet.write(row_num + 1, 14, instance.tl_user_id.name)
            worksheet.write(row_num + 1, 15, instance.odoo_id.Version)
            worksheet.write(
                row_num + 1, 16, ", ".join(instance.perimeters_ids.mapped("name"))
            )
            worksheet.write(row_num + 1, 17, instance.perimeters_number)

        # Save to BytesIO
        output = BytesIO()
        workbook.save(output)
        output.seek(0)

        # Return the file
        file_data = output.read()
        output.close()
        filename = "instance_requests.xls"
        # Return Excel file
        attachment = self.env["ir.attachment"].create(
            {
                "name": filename,
                "type": "binary",
                "res_model": "kzm.instance.request",
                "res_id": self.id,
                "datas": base64.b64encode(file_data),
                "store_fname": filename,  # This is important for downloading the file
            }
        )

        # Force the file to be downloaded
        response = {
            "type": "ir.actions.act_url",
            "url": f"/web/content/{attachment.id}?download=true",
            "target": "self",
        }
        return response

    def action_export_selected(self, records):
        # Create an Excel workbook and add a worksheet
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output)
        worksheet = workbook.add_worksheet()

        # Add headers
        headers = [
            "Reference",
            "Designation",
            "IP Address",
            "Active",
            "CPU",
            "RAM",
            "Disk",
            "URL",
            "Status",
            "Limit Date",
            "Treatment Date",
            "Treatment Duration",
            "Client",
            "Employee",
            "User",
            "Odoo Version",
            "Perimeter IDs",
            "Perimeters Number",
        ]
        for col_num, header in enumerate(headers):
            worksheet.write(0, col_num, header)

        # Add data
        for row_num, instance in enumerate(records):
            worksheet.write(row_num + 1, 0, instance.seq_name)
            worksheet.write(row_num + 1, 1, instance.name)
            worksheet.write(row_num + 1, 2, instance.adress_ip)
            worksheet.write(row_num + 1, 3, instance.active)
            worksheet.write(row_num + 1, 4, instance.cpu)
            worksheet.write(row_num + 1, 5, instance.ram)
            worksheet.write(row_num + 1, 6, instance.disk)
            worksheet.write(row_num + 1, 7, instance.url)
            worksheet.write(row_num + 1, 8, instance.state)
            worksheet.write(row_num + 1, 9, instance.limit_date)
            worksheet.write(row_num + 1, 10, instance.treat_date)
            worksheet.write(row_num + 1, 11, instance.treat_duration)
            worksheet.write(row_num + 1, 12, instance.partner_id.name)
            worksheet.write(row_num + 1, 13, instance.tl_id.name)
            worksheet.write(row_num + 1, 14, instance.tl_user_id.name)
            worksheet.write(row_num + 1, 15, instance.odoo_id.Version)
            worksheet.write(
                row_num + 1, 16, ", ".join(instance.perimeters_ids.mapped("name"))
            )
            worksheet.write(row_num + 1, 17, instance.perimeters_number)

        # Close the workbook

        output = BytesIO()
        workbook.save(output)
        output.seek(0)

        # Return the file
        file_data = output.read()
        output.close()
        filename = "instance_requests.xls"
        # Return Excel file
        attachment = self.env["ir.attachment"].create(
            {
                "name": filename,
                "type": "binary",
                "res_model": "kzm.instance.request",
                "res_id": self.id,
                "datas": base64.b64encode(file_data),
                "store_fname": filename,  # This is important for downloading the file
            }
        )

        # Force the file to be downloaded
        response = {
            "type": "ir.actions.act_url",
            "url": f"/web/content/{attachment.id}?download=true",
            "target": "self",
        }
        return response

    def exportall(self, records):
        return self.action_export_selected(records)
