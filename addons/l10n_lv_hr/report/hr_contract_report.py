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

from report import report_sxw
from osv import osv

import os
import addons
from tools.translate import _
from datetime import datetime


class hr_contract_report(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context=None):
        super(hr_contract_report, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'cr': cr,
            'uid': uid,
            'user':self.pool.get("res.users").browse(cr, uid, uid),
            'datetime': datetime,
            'getLongDate': self.getLongDate,
            'getLongDateFromField': self.getLongDateFromField,
        })
    def getLongDate(self, tm):
        # TODO: move to translation data
        lat_months = [0, u'janvāris', u'februāris', u'marts', u'aprīlis', u'maijs', u'jūnijs', u'jūlijs',
                      u'augusts', u'septembris', u'oktobris', u'novembris', u'decembris']
        return u'%d. gada %d. %s' % (tm.year, tm.day, lat_months[tm.month])
    def getLongDateFromField(self, date_field):
        try:
            zz = datetime.strptime(date_field, '%Y-%m-%d')
        except Exception:
            return False
        return self.getLongDate(zz)        

report_sxw.report_sxw('report.hr.employee.contract', 'hr.contract', 'addons/l10n_lv_hr/report/hr_contract_report.html', parser=hr_contract_report)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
