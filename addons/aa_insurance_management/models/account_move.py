# -*- coding: utf-8 -*-
from odoo import models, fields


class AccountMove(models.Model):
   
    _inherit = 'account.move'

    insurance_id = fields.Many2one('insurance.details',
                                   string='Insurance',
                                   help="Give the insurance details in invoice")
    claim_id = fields.Many2one('claim.details', string='Insurance Claim',
                               help="Give the claim details")
