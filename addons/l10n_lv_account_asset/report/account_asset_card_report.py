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
from osv import osv

class account_asset_card_report(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(account_asset_card_report, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'time': time,
            'cr':cr,
            'uid': uid,
        })
        
report_sxw.report_sxw('report.l10n_lv_account_asset.card',
                       'account.asset.asset', 
                       'addons/l10n_lv_account_asset/report/account_asset_card_report_html.mako',
                       parser=account_asset_card_report)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
