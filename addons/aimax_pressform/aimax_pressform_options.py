##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>).
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

class ampf_pfoptions(osv.osv):

    def _name_get_fnc(self, cr, uid, ids, prop, unknow_none, context=None):
        res = self.name_get(cr, uid, ids, context=context)
        return dict(res)

    _name = 'ampf.pfoptions'
    _columns = {
        'name': fields.char('Options name', size=25),
        #'options_id': fields.many2one('product.product', 'Options Id', required=True, ondelete='cascade'),
        'descriptions': fields.char('Descriptins', size=128),
    }
ampf_pfoptions()



class product_product(osv.osv):
    _name = 'product.product'
    _inherit = 'product.product'
    _columns = {
         #'pf_options_ids': fields.one2many('ampf.pfoptions', 'options_id', 'Options'),
         'apf_options_ids': fields.many2many('ampf.pfoptions','product_printoptions_rel', 'product_id' , 'options_id', 'Options'),
         'apf_rawmaterial_ids': fields.many2many('product.product','product_rawmaterial_rel', 'product_id' , 'rawmaterail_id', 'RAW material'),

         }
product_product()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: