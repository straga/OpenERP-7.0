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

from openerp.osv import fields, osv
from tools.translate import _

class res_partner_bank(osv.osv):
    _inherit = "res.partner.bank"
    _columns = {
        'bank_statement_ids': fields.one2many('account.bank.statement', 'bank_account_id', 'Bank Statements')
    }

    def unlink(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        for rec in self.browse(cr, uid, ids, context=context):
            if rec.bank_statement_ids:
                raise osv.except_osv(_('Invalid action !'), _('Cannot delete a Bank Account, if it has Bank Statements related to it. Please try to delete the related Bank Statements (if possible) and try again!'))
        return super(res_partner_bank, self).unlink(cr, uid, ids, context=context)

res_partner_bank()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
