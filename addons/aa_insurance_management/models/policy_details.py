# -*- coding: utf-8 -*-
from odoo import fields, models


class PolicyDetails(models.Model):
    """This class creates a model 'policy.details' and added fields """
    _name = 'policy.details'
    _description = "Policy Details"

    name = fields.Char(string='Name', required=True,
                       help="Give the policy name")
    policy_type_id = fields.Many2one(
        'policy.type', string='Policy Type', required=True,
        help="Select the policy type")
    payment_type_ids = fields.Many2many('payment.type',
                                        help="Select the policy types")
    currency_id = fields.Many2one(
        'res.currency', string='Currency', required=True,
        default=lambda self: self.env.user.company_id.currency_id.id,
        help="Select the currency")
    amount = fields.Monetary(string='Amount', required=True,
                             help="Give the amount for the policy")
    note_field = fields.Html(string='Comment', help="Specify the comments")
