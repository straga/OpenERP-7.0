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

class account_chart_report(osv.osv_memory):
    _name = "account.chart.report"
    _description = "Chart of Accounts Report"
    _columns = {
        'chart_account_id': fields.many2one('account.account', 'Chart of Account', help='Select Charts of Accounts', required=True, domain = [('parent_id','=',False)])
    }

    def _get_account(self, cr, uid, context=None):
        accounts = self.pool.get('account.account').search(cr, uid, [('parent_id', '=', False)], limit=1)
        return accounts and accounts[0] or False

    _defaults = {
            'chart_account_id': _get_account
    }

    def onchange_chart_id(self, cr, uid, ids, chart_account_id, context=None):
        if not chart_account_id:
            return {}
        return {}

    def _build_contexts(self, cr, uid, ids, data, context=None):
        if context is None:
            context = {}
        result = {}
        result['chart_account_id'] = 'chart_account_id' in data['form'] and data['form']['chart_account_id'] or False
        return result

    def print_report(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        data = {}
        data['ids'] = context.get('active_ids', [])
        data['model'] = context.get('active_model', 'ir.ui.menu')
        data['form'] = self.read(cr, uid, ids, ['chart_account_id'], context=context)[0]
        for field in ['chart_account_id']:
            if isinstance(data['form'][field], tuple):
                data['form'][field] = data['form'][field][0]
        used_context = self._build_contexts(cr, uid, ids, data, context=context)
        data['form']['used_context'] = used_context
        return {'type': 'ir.actions.report.xml', 'report_name': 'l10n_lv_account.chart', 'datas': data}

account_chart_report()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
