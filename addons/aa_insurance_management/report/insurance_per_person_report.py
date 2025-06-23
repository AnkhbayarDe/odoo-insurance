from odoo import api, models

class ReportInsurancePerPerson(models.AbstractModel):
    _name = 'report.aa_insurance_management.insurance_per_person_report'
    _description = 'Insurance Per Person Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        insurances = self.env['insurance.details'].browse(docids)
        partner_insurances = []
        for insurance in insurances:
            partner_insurances.append({
                'customer': insurance.partner_id.name if insurance.partner_id else '',
                'name': insurance.name,
                'policy': insurance.policy_id.name if insurance.policy_id else '',
                'agent': insurance.employee_id.name if insurance.employee_id else '',
                'currency': insurance.currency_id.name if insurance.currency_id else '',
                'amount': insurance.amount,
                'state': insurance.state,
            })
        return {
            'doc_ids': insurances.ids,
            'doc_model': 'insurance.details',
            'docs': insurances,
            'partner_insurances': partner_insurances,
        }