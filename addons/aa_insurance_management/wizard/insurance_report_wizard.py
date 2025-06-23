from odoo import models, fields, api

class InsuranceReportWizard(models.TransientModel):
    _name = 'insurance.report.wizard'
    _description = 'Insurance Report Wizard'
    start_date = fields.Date(string="Start Date", required=True)
    end_date = fields.Date(string="End Date", required=True)
    policy_type_id = fields.Many2one('policy.type', string="Policy Type")

    def generate_report(self):
        data = {
            'form': self.read()[0]
        }
        return self.env.ref('insurance_management_cybro.insurance_policy_report_action').report_action(self, data=data)
