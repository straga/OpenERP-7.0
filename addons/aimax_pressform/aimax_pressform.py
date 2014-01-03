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

class product_product(osv.osv):
    _name = 'product.product'
    _inherit = 'product.product'
    _columns = {
        'apf_aimax_id':fields.char('Aimax id', size=10),
        'apf_grins_id':fields.char('Grins id', size=10),
        'apf_partner_id': fields.many2one('res.partner', 'Owner', change_default=True, select=True),
        'apf_comments': fields.text('Comments'),
        'apf_blank_width': fields.integer('Width', size=5, help="Width blank in mm"),
        'apf_blank_length': fields.integer('Length', size=5, help="Length blank in mm"),
        'apf_it_pressform': fields.boolean('It Press Form', help="Determine if the it Press Form"),
        'apf_on_blank': fields.integer('On Blank', size=5, help="Product on blank"),

        }

product_product()

