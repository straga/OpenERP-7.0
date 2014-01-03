# -*- coding: utf-8 -*-
from osv import fields, osv

import logging
from openerp.tools.translate import _
#import time
#import datetime

_logger = logging.getLogger(__name__)


# Основной проект
class fabric(osv.osv):

    _name = "fabric"
    _description = "Fabric project"
    _columns = {

        'id_fabric': fields.char('ID fabric', size=15, required=True),
        'name': fields.char('Fabric Name', size=128, required=True),
        'description': fields.text('Description'),
        #'link_product': fields.many2one('product.product', 'Link Product', change_default=True, select=True),
        #'fsize_h': fields.integer('size H', required=True, help="Size H for new fabrik product"),
        #'fsize_w': fields.integer('size W', required=True, help="Size W for new fabrik product"),
        #'fsize_z': fields.integer('size Z', required=True, help="Size Z for new fabrik product"),
        #'link_fabric_circulation': fields.one2many('fabric.circulation', 'fabric_id', 'Fabric Circulation'),
        'link_fdesign': fields.one2many('fdesign', 'link_fabric_id', 'Fabric Design'),
        #'link_fabric_design': fields.many2many('fabric.design','fabric_main_design_rel', 'fabric_id' , 'design_id', 'Design'),
        'state': fields.selection([('cancel', 'Cancelled'),('draft', 'Draft'),('confirmed', 'Confirmed'),('exception', 'Exception'),('done', 'Done')], 'Status', required=True, readonly=True,),

        }

    _defaults = {

        'state': 'draft',

        }

fabric()


# # Варианты тиражей для предложения клиета
# class fabric_circulation(osv.osv):
#     _name = "fabric.circulation"
#     _description = "fabric circulation"
#     _order = 'circulation_seq'
#     _columns = {
#
#         'name': fields.char('Fabric Name', size=128, required=False),
#         'description': fields.text('Description'),
#         'fabric_id': fields.many2one('fabric', 'Id', select=True),
#         'circulation_seq': fields.integer('Sequence', required=True, help="Sequence"),
#         'circulation_qty': fields.integer('Quantity', required=True, help="Pre Quantity circulation "),
#         'circulation_unit_cost': fields.float('Unit Cost', required=True, help="Unit Cost "),
#         'circulation_total_cost': fields.float('Total Cost', required=True, help="Total Cost "),
#
#     }
#
#     _defaults = {
#         'circulation_seq': lambda *a: 1,
#     }
#
#
# # Во время добавления тиражей для предложения клиета, делается поверка(кол. предложений не больши трех.)
#     def create(self, cr, uid, vals, context=None):
#
#         #
#         #_logger.warning("vals %s", vals )
#
#         fabric_id = vals['fabric_id']  # get from context ID - is it id fabric
#
#         # Select max seq from circulation for fabric.main. it be max 3. it mean 3 sales quatation.
#         cr.execute('select MAX(circulation_seq) from fabric_circulation where fabric_id=%s', (fabric_id,))
#         seq_list = map(lambda x: x[0], cr.fetchall()) # convert from [2,] to [2]
#
#         #
#         #_logger.warning("seq_list %s", seq_list )
#
#         if str(seq_list) == '[None]': # if not records in data base firs element set 0.
#             seq_int = 0
#         else:
#             seq_int = int(''.join(map(str,seq_list)))     # list to int
#
#         #
#
#         #_logger.warning("seq_int %s", seq_int )
#
#         if seq_int < 3: # +1 if < 3. and add record to database. esle Warning massage !
#             vals['circulation_seq'] = seq_int + 1
#             it_ok = super(fabric_circulation, self).create(cr, uid, vals, context=context)
#         else:
#             raise osv.except_osv(_('Warning!'), "You cannot add more '" + str(seq_int) +"'entry. MAX = 3.")
#
#         return it_ok
#
#
# fabric_circulation()


##-------------- many2many Didirectional for Main Project and Design.
#------1-------
# Ссылка на конструкцию.

# class fabric(osv.osv):
#     _inherit = 'fabric'
#     _columns = {
#         'link_design': fields.many2many(
#             'fdesign',
#             'fabric_fdesign_rel',
#             'fabric_id',
#             'design_id',
#             'Fabric Design'),
#         }
# fabric()






