from odoo import models

class CustomerCardReport(models.AbstractModel):
    _name = 'report.aa_insurance_management.report_patient_detail'
    _description = 'Customer Card PDF'

    def _get_report_values(self, docids, data=None):
        docs = self.env['insurance.details'].browse(docids)
        return {
            'doc_ids': docids,
            'doc_model': 'insurance.details',
            'docs': docs,
            'doc': docs[0] if docs else None,
        }