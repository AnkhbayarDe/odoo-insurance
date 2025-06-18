from odoo import models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'

    insurance_details_ids = fields.One2many(
        'insurance.details',
        'partner_id',
        string='Insurance Details'
    )
