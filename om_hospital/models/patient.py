from odoo import api, fields, models
#from odoo.osv import expression
#from odoo.exceptions import UserError, ValidationError


class HospitalPatientDetails(models.Model):
    _name = "hospital.patient.details"
    _description = "patients"

    name = fields.Char(string='Name')
    age = fields.Integer(string='Age')
    blood_group = fields.Char(string='Blood')
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string='Gender')

    # include_initial_balance = fields.Boolean(string="Bring Accounts Balance Forward", help="Used in reports to know if we should consider journal items from the beginning of time instead of from the fiscal year only. Account types that should be reset to zero at each new fiscal year (like expenses, revenue..) should not have this option set.")
    # type = fields.Selection([
    #     ('other', 'Regular'),
    #     ('receivable', 'Receivable'),
    #     ('payable', 'Payable'),
    #     ('liquidity', 'Liquidity'),
    # ], required=True, default='other',
    #     help="The 'Internal Type' is used for features available on "\
    #     "different types of accounts: liquidity type is for cash or bank accounts"\
    #     ", payable/receivable is for vendor/customer accounts.")