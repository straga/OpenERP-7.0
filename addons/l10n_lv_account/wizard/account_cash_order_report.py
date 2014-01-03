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

from osv import fields, osv

class account_cash_order_report(osv.osv_memory):
    _name = "account.cash.order.report"
    _description = "Cash Order Report"

    _columns = {
        'report_line_ids': fields.many2many('account.bank.statement.line', 'account_bank_statement_line_rel', 'report_line_id', 'line_id', 'Cash Book Lines', help='Select a Cash Register Line to print the Order from')
    }

account_cash_order_report()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
