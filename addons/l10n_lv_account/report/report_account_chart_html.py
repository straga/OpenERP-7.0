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

class report_account_chart_html(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(report_account_chart_html, self).__init__(cr, uid, name, context=context)
        self.result_acc = []
        self.localcontext.update({
            'time': time,
            'cr':cr,
            'uid': uid,
            'lines': self.lines,
            'get_account': self._get_account,
        })
        self.context = context

    def set_context(self, objects, data, ids, report_type=None):
        new_ids = ids
        if (data['model'] == 'ir.ui.menu'):
            new_ids = 'chart_account_id' in data['form'] and [data['form']['chart_account_id']] or []
            objects = self.pool.get('account.account').browse(self.cr, self.uid, new_ids)
        return super(report_account_chart_html, self).set_context(objects, data, new_ids, report_type=report_type)

    def _get_account(self, data):
        if data['model']=='account.account':
            return self.pool.get('account.account').browse(self.cr, self.uid, data['form']['id'])
        return super(report_account_chart_html ,self)._get_account(data)

    def lines(self, form, ids=[], done=None):#, level=1):
        def _process_child(accounts, parent):
                account_rec = [acct for acct in accounts if acct['id']==parent][0]
                currency_obj = self.pool.get('res.currency')
                acc_id = self.pool.get('account.account').browse(self.cr, self.uid, account_rec['id'])
                currency = acc_id.currency_id.name or acc_id.company_currency_id.name
                res = {
                    'id': account_rec['id'],
                    'type': account_rec['type'],
                    'code': account_rec['code'],
                    'name': account_rec['name'],
                    'currency': currency,
                    'active': account_rec['active'],
                    'parent_id': account_rec['parent_id']
                }
                self.result_acc.append(res)
                if account_rec['child_id']:
                    for child in account_rec['child_id']:
                        _process_child(accounts,child)

        obj_account = self.pool.get('account.account')
        if not ids:
            ids = self.ids
        if not ids:
            return []
        if not done:
            done={}

        ctx = self.context.copy()

        parents = ids
        child_ids = obj_account._get_children_and_consol(self.cr, self.uid, ids, ctx)
        if child_ids:
            ids = child_ids
        accounts = obj_account.read(self.cr, self.uid, ids, ['type','code','name','currency_id', 'company_currency_id','active','parent_id','child_id'], ctx)

        for parent in parents:
                if parent in done:
                    continue
                done[parent] = 1
                _process_child(accounts,parent)
        return self.result_acc

report_sxw.report_sxw('report.l10n_lv_account.chart',
                       'account.account', 
                       'addons/l10n_lv_account/report/report_account_chart_html.mako',
                       parser=report_account_chart_html)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

