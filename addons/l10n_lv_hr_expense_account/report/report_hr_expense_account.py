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

import time
from report import report_sxw
from osv import osv
from tools.translate import _

class report_hr_expense_account_html(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(report_hr_expense_account_html, self).__init__(cr, uid, name, context=context)
        self.result_exp = []
        self.result_bank = []
        self.localcontext.update({
            'time': time,
            'cr':cr,
            'uid': uid,
            'lines': self.lines,
            'bank_lines': self.bank_lines
        })
        self.context = context

    def bank_lines(self, form, ids=[]):
        bank_obj = self.pool.get('account.bank.statement.line')
        self.result_bank = bank_obj.browse(self.cr, self.uid, form['bank_statement_line_ids'])
        return self.result_bank

    def lines(self, form, ids=[]):
        expense_obj = self.pool.get('hr.expense.expense')
        exp_ids = expense_obj.search(self.cr, self.uid, [('date','>=',form['date_from']),('date','<=',form['date_to']),('employee_id','=',form['employee_id']),('account_move_id','!=',False)])
        self.result_exp = expense_obj.browse(self.cr, self.uid, exp_ids)
        return self.result_exp

report_sxw.report_sxw('report.l10n_lv_hr_expense_account.report1',
                       'hr.expense.expense', 
                       'addons/l10n_lv_hr_expense_account/report/report_hr_expense_account.mako',
                       parser=report_hr_expense_account_html)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
