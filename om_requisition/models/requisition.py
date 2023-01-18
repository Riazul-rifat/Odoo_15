from odoo import api, fields, models
from odoo.exceptions import ValidationError

from datetime import datetime
# Creating the model
# Table for purchase order
class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    # email_from = fields.Char(string='email_from', default='root@yourcompany.example.com')
    # email_to = fields.Char(string='email_to', default='rifat.office928@gmail.com')
    requisition_number = fields.Char('PO Requisition')



# Requisition Table
class CustomPurchaseRequisition(models.Model):
    # name of the table
    _name = "custom.purchase.requisition"
    _inherit = ['mail.thread', 'mail.activity.mixin',]

     # Below name is an automated sequence
    name = fields.Char(string="Custom PO Requisition", required=True, copy=False,readonly=True,index=True,default=lambda self: ('Newest'))
    _description = 'Requisition for purchase'
    warehouse_id = fields.Many2one('stock.warehouse', string='Warehouse', required =True)  #  Select warehouse for the product/ One product can be found in many warehouses
    partner_id = fields.Many2one('res.partner', string='Vendor', required=True,
                                 help=" To find vendor ") # Select product's vendor
    delivery_date = fields.Datetime(
        string='Delivery Date', required=True, index=True)
    po_reference = fields.Many2one('purchase.order', string='PO Reference')
    requisition_orders = fields.One2many('requisition.orders', 'order_id', string='Orders', states={
        'cancel': [('readonly', True)], 'done': [('readonly', True)]}, copy=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('approve', 'Approved'),
        ('cancel', 'Cancelled')
    ],   default='draft', string='Status', required= True)

    email_from = fields.Char(string='email_from', default = 'x@gmail.com')
    email_to = fields.Char(string='email_to', default='y@gmail.com')

    #@api.multi

    def approval(self):

        # Draft to approve
        if self.state=='draft':
            self.state= 'approve'

        else:
            raise ValidationError("Already approved")

        # Creating purchase order
        purchase_order_data = {
                'requisition_number': str(self.name),
                'date_order': fields.datetime.now(),
                'partner_id': self.partner_id.id,

            }
        purchase_order_list = list()
        for item in self.requisition_orders:
            purchase_order_list.append([0, False,
                                                              {
                                                                  'name': item.product_id.name,
                                                                  'product_id': item.product_id.id,
                                                                  'product_qty': item.product_quantity,
                                                                  'product_uom': item.product_uom.id,
                                                                  'date_planned': fields.datetime.now(),
                                                                  'price_unit': item.product_id.product_tmpl_id.list_price,
                                                              }])

        purchase_order_data['order_line']=purchase_order_list

        # Creating purchase order
        purchase_orders= self.env['purchase.order'].create(purchase_order_data)

        # Updating po reference
        self.write(
            {
                'po_reference': purchase_orders.id
            }
        )

        print(purchase_order_data)

    def action_email(self):
        mail_template = self.env.ref('om_requisition.inherit_purchase_email_template')
        mail_template.send_mail(self.id, force_send=True)

    @api.model
    def create(self, vals):

        if vals.get('name', ('Newest')) == ('Newest'):
            vals['name'] = self.env['ir.sequence'].next_by_code('po.sequence') or ('Newest')
        result = super(CustomPurchaseRequisition, self).create(vals)
        return result

    # Another way to create automated sequence number
    # @api.model
    # def create(self, values):
    #
    #     record = super(Requisition, self).create(values)
    #     record.name = "REQ0" + str(record.id)
    #
    #     return record

    # Requisition delete function
    def delete_requisition(self):
        self.unlink()


class RequisitionOrders(models.Model):
    _name = 'requisition.orders'
    _description = 'Requisition Orders'

    order_id = fields.Many2one(
        'custom.purchase.requisition', string='Order Reference', index=True, required=True, ondelete='cascade')
    name = fields.Text(string='Description')
    product_id = fields.Many2one('product.product', string='Product')
    product_quantity = fields.Float(string='Quantity', required=True)

    product_uom = fields.Many2one(
        'uom.uom', string='Unit of Measure', required=True)
    price = fields.Float(string='Price')

    @api.constrains('product_quantity')
    def _check_date_end(self):
        for record in self:
            if record.product_quantity <=0:
                raise ValidationError("The quantity must be greater than 0")

    @api.onchange('product_id')
    def onchange_product_id(self):
        if self.product_id:
            self.product_uom = self.product_id.uom_po_id

        else:
            self.product_uom = None


