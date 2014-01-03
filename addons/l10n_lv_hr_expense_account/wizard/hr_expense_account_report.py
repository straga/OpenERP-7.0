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
import pooler
from tools.translate import _

class hr_expense_account_report(osv.osv_memory):
    _name = "hr.expense.account.report"
    _description = "HR Expenses Report"

    _columns = {
        'employee_id': fields.many2one('hr.employee', 'Employee', required=True),
        'account_id': fields.many2one('account.account', 'Account', domain="[('type','=','payable')]"),
        'date_from': fields.date('Date From', required=True),
        'date_to': fields.date('Date To', required=True),
        'bank_statement_line_ids': fields.many2many('account.bank.statement.line', 'bank_statement_line_rel', 'report_id', 'statement_line_id', 'Bank Statement Lines')
    }

    def onchange_data(self, cr, uid, ids, employee_id, account_id, date_from, date_to, context=None):
        if context is None:
            context = {}
        employee = self.pool.get('hr.employee').browse(cr, uid, employee_id, context=context)
        bank_statement_line_ids = self.pool.get('account.bank.statement.line').search(cr, uid, [('partner_id','=',employee.address_home_id.id),('account_id','=',employee.address_home_id.property_account_receivable.id),('date','>=',date_from),('date','<=',date_to)], context=context)
        return {'value': {'bank_statement_line_ids': bank_statement_line_ids}}

    def _build_contexts(self, cr, uid, ids, data, context=None):
        if context is None:
            context = {}
        result = {}
        result['employee_id'] = 'employee_id' in data['form'] and data['form']['employee_id'] or False
        result['account_id'] = 'account_id' in data['form'] and data['form']['account_id'] or False
        result['date_from'] = 'date_from' in data['form'] and data['form']['date_from'] or False
        result['date_to'] = 'date_to' in data['form'] and data['form']['date_to'] or False
        result['bank_statement_line_ids'] = 'bank_statement_line_ids' in data['form'] and data['form']['bank_statement_line_ids'] or False
        return result

    def print_report(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        data = {}
        data['ids'] = context.get('active_ids', [])
        data['model'] = context.get('active_model', 'ir.ui.menu')
        data['form'] = self.read(cr, uid, ids, ['employee_id','account_id','date_from','date_to', 'bank_statement_line_ids'], context=context)[0]
        for field in ['employee_id','account_id','date_from','date_to','bank_statement_line_ids']:
            if isinstance(data['form'][field], tuple):
                data['form'][field] = data['form'][field][0]
        used_context = self._build_contexts(cr, uid, ids, data, context=context)
        data['form']['used_context'] = used_context
        return {'type': 'ir.actions.report.xml', 'report_name': 'l10n_lv_hr_expense_account.report1', 'datas': data}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
