from odoo import api, fields, models, _, tools


class MrpRoutingWorkcenter(models.Model):
    _inherit = 'mrp.routing.workcenter'
    cost = fields.Float(string='Total cost',readonly=True, compute='_compute_total_cost', store=True)
    wc_cost_per_minute = fields.Float(related='workcenter_id.cost_per_min', string='Work Center Cost(Min)')

    @api.depends('time_cycle','workcenter_id.cost_per_min')
    def _compute_total_cost(self):
        for record in self:
            record.cost=record.workcenter_id.cost_per_min * record.time_cycle
