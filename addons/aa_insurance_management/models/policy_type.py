# -*- coding: utf-8 -*-
from odoo import fields, models


class PolicyType(models.Model):
    """This class creates a model 'policy.type' and added fields """
    _name = 'policy.type'
    _description = "Policy Type"

    name = fields.Char(string='Name', help="Give the policy type")
