from odoo import api, fields, models
# Creating the model


class MrpWorkcenter(models.Model):
    _inherit = 'mrp.workcenter'

    user_id = fields.Many2one('res.users',  string='Responsible person',  required=True)

