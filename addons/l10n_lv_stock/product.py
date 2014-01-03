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
from tools.translate import _
import openerp.addons.decimal_precision as dp

class product_product(osv.osv):
    _inherit = "product.product"

    _columns = {
        'qty_available2': fields.float('Quantity On Hand 2', digits_compute=dp.get_precision('Product Unit of Measure')),
        'virtual_available2': fields.float('Quantity Available 2', digits_compute=dp.get_precision('Product Unit of Measure'))
    }

    def check_product_qty(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        for product in self.browse(cr, uid, ids, context=context):
            if product.qty_available2 != product.qty_available:
                product.write({'qty_available2': product.qty_available})
            if product.virtual_available2 != product.virtual_available:
                product.write({'virtual_available2': product.virtual_available})
        return True

    def search(self, cr, uid, args, offset=0, limit=None, order=None, context=None, count=False):
        if context.get('refresh_cache'):
            context['refresh_cache'] = False
            prod_ids = self.search(cr, uid, [], context=context)
            self.check_product_qty(cr, uid, prod_ids, context=context)
        return super(product_product, self).search(cr, uid, args, offset, limit, order, context=context, count=count)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
