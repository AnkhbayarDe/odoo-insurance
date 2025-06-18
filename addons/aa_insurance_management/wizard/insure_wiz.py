from odoo import models, fields

class InsuranceReport2Wizard(models.TransientModel):
    _name = 'insure.wiz'
    _description = 'Insurance Report2 Wizard'

    start_date = fields.Date(string="Start Date", required=True)
    end_date = fields.Date(string="End Date", required=True)
    policy_type_id = fields.Many2one('policy.type', string="Policy Type")

    def action_generate(self):
        data = {'form': self.read()[0]}
        return self.env.ref('insurance_management_cybro.insurance_policy_report_action').report_action(self, data=data)
        