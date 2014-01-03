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

class account_asset_turnover(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(account_asset_turnover, self).__init__(cr, uid, name, context=context)
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
        asset_ids = asset_obj.search(self.cr, self.uid, [('confirmation_date','<=',form['to_date']),('confirmation_date','!=',False),'|',('close_date','=',False),('close_date','>=',form['from_date'])], order='category_id')
        assets = asset_obj.browse(self.cr, self.uid, asset_ids)

        datas1 = {}
        result1 = []

        purchase1 = 0.0
        depr1 = 0.0
        left1 = 0.0
        purchase2 = 0.0
        depr2 = 0.0
        left2 = 0.0
        purchase3 = 0.0
        depr3 = 0.0
        left3 = 0.0
        purchase4 = 0.0
        depr4 = 0.0
        left4 = 0.0
        purchase_total1 = 0.0
        depr_total1 = 0.0
        left_total1 = 0.0
        purchase_total2 = 0.0
        depr_total2 = 0.0
        left_total2 = 0.0

        for asset in assets:
            account_id = asset.category_id.account_asset_id.id
            account_code = asset.category_id.account_asset_id.code
            account_name = asset.category_id.account_asset_id.name
            depr_1 = 0.0
            for line in asset.depreciation_line_ids:
                if line.move_check == True and line.depreciation_date < form['from_date']:
                    depr_1 += line.amount
            depr1 = depr_1
            if asset.confirmation_date < form['from_date']:
                purchase1 = asset.purchase_value
                left1 = asset.purchase_value - depr1
            else:
                purchase1 = 0.0
                left1 = 0.0
            if asset.confirmation_date >= form['from_date']:
                purchase2 = asset.purchase_value
                left2 = asset.purchase_value
            else:
                purchase2 = 0.0
                left2 = 0.0
            depr_3 = 0.0
            for line in asset.depreciation_line_ids:
                if line.move_check == True and line.depreciation_date >= form['from_date'] and line.depreciation_date <= form['to_date']:
                    depr_3 += line.amount
            depr3 = depr_3
            left3 = purchase3 - depr3
            if asset.close_date <= form['to_date'] and asset.close_date != False:
                depr = 0.0
                for line in asset.depreciation_line_ids:
                    if line.move_check == True:
                        depr += line.amount
                purchase4 = - asset.purchase_value
                depr4 = - depr
                left4 = - (asset.purchase_value - depr)
            else:
                purchase4 = 0.0
                depr4 = 0.0
                left4 = 0.0
            purchase_total1 = purchase2 + purchase3 + purchase4
            depr_total1 = depr2 + depr3 + depr4
            left_total1 = left2 + left3 + left4
            purchase_total2 = purchase1 + purchase2 + purchase3 + purchase4
            depr_total2 = depr1 + depr2 + depr3 + depr4
            left_total2 = left1 + left2 + left3 + left4
            if datas1.get((account_id)):
                purchase1 += datas1[(account_id)]['purchase1']
                left1 += datas1[(account_id)]['left1']
                depr1 += datas1[(account_id)]['depr1']
                purchase2 += datas1[(account_id)]['purchase2']
                left2 += datas1[(account_id)]['left2']
                depr3 += datas1[(account_id)]['depr3']
                left3 += datas1[(account_id)]['left3']
                purchase4 += datas1[(account_id)]['purchase4']
                depr4 += datas1[(account_id)]['depr4']
                left4 += datas1[(account_id)]['left4']
                purchase_total1 += datas1[(account_id)]['purchase_total1']
                depr_total1 += datas1[(account_id)]['depr_total1']
                left_total1 += datas1[(account_id)]['left_total1']
                purchase_total2 += datas1[(account_id)]['purchase_total2']
                depr_total2 += datas1[(account_id)]['depr_total2']
                left_total2 += datas1[(account_id)]['left_total2']
                datas1[(account_id)].clear()
            if not datas1.get((account_id)):
                datas1[(account_id)] = {'account_id': account_id, 'account_code': account_code, 'account_name': account_name, 'purchase1': purchase1, 'depr1': depr1, 'left1': left1, 'purchase2': purchase2, 'depr2': depr2, 'left2': left2, 'purchase3': purchase3, 'depr3': depr3, 'left3': left3, 'purchase4': purchase4, 'depr4': depr4, 'left4': left4, 'purchase_total1': purchase_total1, 'depr_total1': depr_total1, 'left_total1': left_total1, 'purchase_total2': purchase_total2, 'depr_total2': depr_total2, 'left_total2': left_total2}
            result1.append(datas1[(account_id)])
        
        for object in result1:
            if object != {}:
                self.result_asset.append(object)

        return self.result_asset
        
report_sxw.report_sxw('report.l10n_lv_account_asset.turnover',
                       'account.asset.asset', 
                       'addons/l10n_lv_account_asset/report/account_asset_turnover_report_html.mako',
                       parser=account_asset_turnover)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
