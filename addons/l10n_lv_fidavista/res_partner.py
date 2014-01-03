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

from openerp.osv import osv, fields
from openerp.tools.translate import _

class res_partner(osv.osv):
    _inherit = "res.partner"

    def _default_property_account_receivable(self, cr, uid, context=None):
        if context is None:
            context = {}
        account_id = self.pool.get('account.account').search(cr, uid, [('code','=','2310')], context=context)
        if account_id:
            return account_id[0]
        return False

    def _default_property_account_payable(self, cr, uid, context=None):
        if context is None:
            context = {}
        account_id = self.pool.get('account.account').search(cr, uid, [('code','=','5310')], context=context)
        if account_id:
            return account_id[0]
        return False

    _defaults = {
        'property_account_receivable': _default_property_account_receivable,
        'property_account_payable': _default_property_account_payable
    }

res_partner()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
