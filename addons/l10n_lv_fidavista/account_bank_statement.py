# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2012 ITS-1 (<http://www.its1.lv/>)
#                       E-mail: <info@its1.lv>
#                       Address: <Vienibas gatve 109 LV-1058 Riga Latvia>
#                       Phone: +371 66116534
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.osv import fields, osv

class account_bank_statement(osv.osv):
    _inherit = "account.bank.statement"
    _columns = {
        'bank_account_id': fields.many2one('res.partner.bank', 'Bank Account', ondelete='restrict', select=True)
    }

account_bank_statement()

class account_bank_statement_line(osv.osv):
    _inherit = "account.bank.statement.line"

    _columns = {
        'transaction_type': fields.char('Trans. Type Code', size=4, readonly="1"),
        'partner_name': fields.char('Partner Name', size=64, readonly="1"),
        'partner_reg_id': fields.char('Partner Registration Number', size=32),
        'partner_bank_account': fields.char('Partner Bank Account Number', size=32)
    }

account_bank_statement_line()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
