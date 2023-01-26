from odoo import api, fields, models
from odoo.exceptions import ValidationError
# Creating the model


class MrpWorkcenter(models.Model):
    _inherit = 'mrp.workcenter'

    user_id = fields.Many2one('res.users', string='Responsible person',  required=True)
    total_prod_capacity = fields.Float(string='Total Production Capacity(min)', required=True)
    rental_cost = fields.Float(string='Rental Cost', required=True)
    labor_cost = fields.Float(string='Labor Cost', required=True)
    common_area_cost = fields.Float(string='Common area cost', required=True)
    cost_per_min = fields.Float(string='Cost Per Minute', readonly=True, required=True, compute='_compute_cost_per_minute')


    @api.constrains('total_prod_capacity', 'rental_cost', 'labor_cost', 'common_area_cost')
    def _check_values(self):
        for record in self:
            if record.total_prod_capacity <1:
                raise ValidationError("Production capacity must be greater than or equal to one ")

            if record.rental_cost < 0:
                raise ValidationError("Rental cost can't be negative")

            if record.labor_cost <0:
                raise ValidationError("Labor cost can't be negative")

            if record.common_area_cost <0:
                raise ValidationError("Common area cost can't be negative")



    @api.depends('total_prod_capacity','rental_cost','labor_cost','common_area_cost')
    def _compute_cost_per_minute(self):
        cc_rc_lc = self.common_area_cost+self.rental_cost+self.labor_cost
        try:
            if cc_rc_lc/self.total_prod_capacity:
                total_cost = cc_rc_lc/self.total_prod_capacity
        except ZeroDivisionError as e:
            raise ValidationError(' Zero division error ')
        #total_cost =(self.common_area_cost+self.rental_cost+self.labor_cost)/self.total_prod_capacity
        self.cost_per_min = total_cost
