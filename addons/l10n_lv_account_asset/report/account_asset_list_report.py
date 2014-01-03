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
from datetime import datetime
from report import report_sxw
from osv import osv, fields

class account_asset_list(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(account_asset_list, self).__init__(cr, uid, name, context=context)
        self.result_asset = []
        self.localcontext.update({
            'time': time,
            'cr':cr,
            'uid': uid,
            'lines': self.lines,
        })
        self.context = context

    def lines(self, form, ids=[]):
        asset_obj = self.pool.get('account.asset.asset')
        asset_ids = asset_obj.search(self.cr, self.uid, [('confirmation_date','<=',form['date']),('confirmation_date','!=',False),'|',('close_date','=',False),('close_date','>=',form['date'])], order='category_id')
        self.result_asset = asset_obj.browse(self.cr, self.uid, asset_ids)
        return self.result_asset

report_sxw.report_sxw('report.l10n_lv_account_asset.list',
                       'account.asset.asset', 
                       'addons/l10n_lv_account_asset/report/account_asset_list_report_html.mako',
                       parser=account_asset_list)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
