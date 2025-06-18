from odoo import api, models

class ReportInsurancePerPerson(models.AbstractModel):
    _name = 'report.aa_insurance_management.insurance_per_person_report'
    _description = 'Insurance Per Person Report'
    

    @api.model
    def _get_report_values(self, docids, data=None):
        partners = self.env['res.partner'].browse(docids)
        # Assuming you have a One2many or Many2many from partner to insurance.details
        return {
            'doc_ids': partners.ids,
            'doc_model': 'res.partner',
            'docs': partners,
        }