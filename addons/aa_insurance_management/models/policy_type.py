# -*- coding: utf-8 -*-
from odoo import fields, models


class PolicyType(models.Model):
    _name = 'policy.type'
    _description = "Policy Type"

    name = fields.Char(string='Name', help="Give the policy type")
