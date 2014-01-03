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

import tools
from osv import  osv, fields
import os
from tools.translate import _

class wizard_fidavista_config(osv.osv_memory):

    _name='wizard.fidavista.config'
    _inherit = 'res.config'

    def execute(self, cr, uid, ids, context=None):
        if context is None:
            context = {}

        account_obj = self.pool.get('account.account')
        account_5310 = account_obj.search(cr, uid, [('code','=','5310')], context=context)
        account_7750 = account_obj.search(cr, uid, [('code','=','7750')], context=context)
        account_2611 = account_obj.search(cr, uid, [('code','=','2611')], context=context)
        account_2310 = account_obj.search(cr, uid, [('code','=','2310')], context=context)

        trans_type_obj = self.pool.get('account.fidavista.transaction.type')
        if account_5310:
            trans_type_obj.create(cr, uid, {'type': 'OUTP, NMSC, NINT, MEMD, IZEJOŠAIS KLĪRINGA MAKSĀJUMS, IZEJOŠAIS MAKSĀJUMS', 'account_id': account_5310[0], 'io': '-'}, context=context)
        if account_7750:
            trans_type_obj.create(cr, uid, {'type': 'OTHR, NFEX, NCHG, KLĪRINGA KOMISIJA', 'account_id': account_7750[0], 'io': '-'}, context=context)
        if account_2611:
            trans_type_obj.create(cr, uid, {'type': 'CHOU', 'account_id': account_2611[0]}, context=context)
        if account_2310:
            trans_type_obj.create(cr, uid, {'type': 'INP, MEMC', 'account_id': account_2310[0], 'io': '+'}, context=context)

wizard_fidavista_config()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
