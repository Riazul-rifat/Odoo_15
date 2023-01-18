from odoo import api, fields, models
from odoo.exceptions import ValidationError

# Product damage Table
class ProductDamage(models.Model):
    # name of the table
    _name = "product.damage"

     # Below name is an automated sequence
    name = fields.Char(string="Damaged Product", required=True, copy=False,readonly=True,index=True,default=lambda self: ('New'))
    company_id = fields.Many2one('res.company', string='Company', required=True)
    product_id = fields.Many2one('product.product', string='Product')
    damage_lines = fields.One2many('product.damage.line', 'damage_id', string='Orders')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirmed'),
    ], default='draft', string='Status', required=True)


    #@api.multi
    def confirmation(self):

        # Draft to approve
        if self.state=='draft':
            self.state= 'confirm'

        else:
            raise ValidationError("Already confirmed")

    @api.model
    def create(self, vals):
        if vals.get('name', ('New')) == ('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('pd.sequence') or ('New')
        result = super(ProductDamage, self).create(vals)
        return result

class ProductDamageLine(models.Model):
    _name = 'product.damage.line'
    serial_id = fields.Integer(string='Serial')
    challan = fields.Char(string='Chalan')
    quantity = fields.Float(string='Quantity')
    price = fields.Float(string='Price')
    vat = fields.Float(string='VAT')
    proposed_price = fields.Float(string='Proposed Price')
    reason = fields.Char(string='Reason')
    damage_id = fields.Many2one('product.damage', string='Damage reference')

    @api.constrains('quantity', 'price', 'vat', 'proposed_price')
    def _check_date_end(self):
        for record in self:
            if record.quantity <= 0:
                raise ValidationError("quantity must be greater than 0")

            if record.price <= 0:
                raise ValidationError("price must be greater than 0")

            if record.vat <0:
                raise ValidationError("vat must be greater or equal to 0")

            if record.proposed_price < record.price + record.vat:
                raise ValidationError("Proposed price should be at least price+vat")

