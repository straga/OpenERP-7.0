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
from dateutil.relativedelta import relativedelta

from osv import osv, fields

from tools.translate import _

class account_asset_set_close_date(osv.osv_memory):
    _name = "account.asset.set.close.date"
    _description = "Set Date Closed for Account Asset"

    _columns = {
        'close_date': fields.date('Date Closed', required=True),
    }

    def set_close_date(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        asset_obj = self.pool.get('account.asset.asset')
        asset_id = context.get('active_id', False)
        asset = asset_obj.browse(cr, uid, asset_id, context=context)
        data = self.browse(cr, uid, ids[0], context=context)

        asset_vals = {
            'close_date': data.close_date
        }
        asset_obj.write(cr, uid, [asset_id], asset_vals, context=context)

        return {'type': 'ir.actions.act_window_close'}

account_asset_set_close_date()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
