from odoo import api, fields, models


# Creating the model


class MrpWorkcenter(models.Model):
    _inherit = 'mrp.workorder'

    resume_time = fields.Datetime(string='Next resume time',)
    state = fields.Selection(
        selection_add=[
            ('pause', 'Paused'),
        ])
