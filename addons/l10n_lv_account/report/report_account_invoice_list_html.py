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

class report_account_invoice_list_html(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(report_account_invoice_list_html, self).__init__(cr, uid, name, context=context)
        self.result_inv = []
        self.localcontext.update({
            'time': time,
            'cr':cr,
            'uid': uid,
            'lines': self.lines,
        })
        self.context = context

    def lines(self, form, ids=[]):
        invoice_obj = self.pool.get('account.invoice')
        inv_ids = invoice_obj.search(self.cr, self.uid, [('type','=',form['invoice_type'])], order='currency_id')
        self.result_inv = invoice_obj.browse(self.cr, self.uid, inv_ids)
        return self.result_inv

report_sxw.report_sxw('report.l10n_lv_account.invoice_list',
                       'account.invoice', 
                       'addons/l10n_lv_account/report/report_account_invoice_list_html.mako',
                       parser=report_account_invoice_list_html)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

