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

from openerp.tools.translate import _
from openerp.osv import fields, osv

class account_fidavista_transaction_type(osv.osv):
    _name = 'account.fidavista.transaction.type'
    _description = 'FiDAViSta Transaction Types'
    _rec_name = 'type'
    _columns = {
        'type': fields.text('Type', required=True, help="Enter FiDAViSta Transaction Type Codes or Transaction Type Names. Please separate by a comma and a space (', '), otherwise the Type won't be found, when importing FiDAViSta file."),
        'io': fields.selection([
            ('+', '+'),
            ('-', '-'),
            ], 'I/O', help="Controls, whether the Amount of the transaction is positive or negative.", select=True),
        'account_id': fields.many2one('account.account', 'Account', required=True, help="The account for the transaction."),
        'description': fields.text('Description')
    }

account_fidavista_transaction_type()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
