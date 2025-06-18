# -*- coding: utf-8 -*-
from odoo import fields, models


class PaymentType(models.Model):
    _name = 'payment.type'
    _description = 'Payment Type'

    name = fields.Char(string="Payment Type",
                              help="Select the policy type")
