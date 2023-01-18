from odoo import api, fields, models
from odoo.exceptions import ValidationError

class IneligibleProduct(models.Model):

    _name = 'ineligible.product.list'

    name = fields.Char(string='Damaged Product', required = True, copy = False, readonly = True, index = True, default= lambda self:('New'))
    company_id = fields.Many2one('res.company', string='Company', required = True)
    product_lines = fields.One2many('inept.products', 'product_line', string='Products')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirmed')
    ], default = 'draft', string='Status', required = True)

    def confirmation(self):
        if self.state=='draft':
            self.state='confirm'
        else:
            raise ValidationError("Already confirmed")


    @api.model
    def create(self, vals):
        if vals.get('name', ('New')) == ('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('ProductUnfit.sequence') or ('New')
        result = super(IneligibleProduct, self).create(vals)
        return result


class IneptProducts(models.Model):
    _name = 'inept.products'

    serial = fields.Integer(string='Serial')
    product_id = fields.Many2one('product.product', string='Products', required = True)
    actual_price = fields.Float(string='Actual Price', required = True)
    proposed_price = fields.Float(string='Proposed Price', required = True)
    product_quantity = fields.Float(string='Product Quantity', required = True)
    product_uom = fields.Many2one('uom.uom', string='Measurement', required = True)
    reason = fields.Char(string='Reason')

    product_line = fields.Many2one('ineligible.product.list', string='Product List')

    @api.constrains('product_quantity', 'actual_price', 'proposed_price')
    def _check_date_end(self):
        for record in self:
            if record.product_quantity <= 0:
                raise ValidationError("quantity must be greater than 0")

            if record.actual_price <= 0:
                raise ValidationError("price must be greater than 0")

            if record.proposed_price < 0:
                raise ValidationError(" Must be greater or equal to 0")



