# -*- coding: utf-8 -*-
from osv import fields, osv

import logging
from openerp.tools.translate import _
#import time
#import datetime

_logger = logging.getLogger(__name__)


class fdstage(osv.osv):

    _name = 'fdstage'
    _description = "Design Stage"
    _order = 'fdstage_seq'

    _columns = {
        
        'name': fields.char('Stage Name', size=128, required=False),
        'description': fields.text('Description'),
        # Conect to fabric design # FIXME dsd

        'fdstage_seq': fields.integer('Sequence', required=True, help="Sequence"),

        'fdesign_id': fields.many2one('fdesign', 'Fabric design', select=True),

        'fdstage_lines_ids': fields.one2many('fdstage.lines', 'fdstage_id', 'Stage Lines'),

        #'fdstage_to_consume_ids': fields.one2many('fdstage.lines', 'to_consume', 'Stage Lines'),

        #'fdstage_to_produce_ids': fields.one2many('fdstage.lines', 'to_produce', 'Stage Lines'),


        }

fdstage()




class fdstage_lines(osv.osv):

    _name = 'fdstage.lines'
    _description = "Design Stage Lines"
    _order = 'lines_seq'


    # def _set_qty_readonly(self, cr, uid, ids, name, arg, context=None):
    #     res = {}
    #     for m in self.browse(cr, uid, ids, context=context):
    #         res['value_diff'] = m.value_now - m.value_last
    #     return {'value':res}
    #
    # def _calculate_total(self, cr, uid, ids, name, args, context):
    #     if not ids: return {}
    #     res = {}
    #     for line in self.browse(cr, uid, ids, context=context):
    #         res[line.id] = float(line.quantity) * line.amount * line.rate / 100
    #     return res

    def _set_qty_readonly(self, cr, uid, ids, product_uom, arg, context=None):
         res = {}

         #For Unit of measure where ID = 13 and 14 - make field qty is readonly

         for m in self.browse(cr, uid, ids, context=context):

             uom_id = int(m.product_uom)
             massiv = [12, 13, 14]
             # ID 13 - Circulation , ID 14 - Blank qnt readonly because dependet from order qnty.
             # and Price for Circulation and Blank get from price depent from qnty
             for massiv_id in massiv:

                if uom_id == massiv_id:
                    res[m.id] = True
                else:
                    res[m.id] = False

             #_logger.error("uom.name %s", uom.name)
             #uom = self.pool.get('product.uom').browse(cr, uid, uom_id, context=context)
             #_logger.error("uom.name %s", uom.name)

         return res

    _columns = {

        #'name': fields.char('Fabric Name', size=128, required=False),
        #'description': fields.text('Description'),
        # Conect to fabric design # FIXME dsd

        'lines_seq': fields.integer('Seq.', required=True, help="Sequence"),

        'name': fields.char('Name', size=64),

        'link_product': fields.many2one('product.product', 'Link Product', change_default=True, select=True),

        'product_uom': fields.many2one('product.uom', 'Unit of Measure', required=False, help="Unit of Measure (Unit of Measure) is the unit of measurement for the inventory control"),

        'qty_readonly': fields.function(_set_qty_readonly, string="Qty Readonly", type='boolean'),


        #'product_uom': fields.many2one('product.uom', 'Product Unit of Measure', required=True, help="Unit of Measure (Unit of Measure) is the unit of measurement for the inventory control"),


        'cost_type': fields.selection([('in_unit', 'In Unit Cost'),('not_in', 'Not in cost'),('in_add_cost', 'Add Cost'),], 'Cost Type', required=True, readonly=False,),

        #requirement
        'req_type': fields.selection([('to_consume', 'To Consume'),('to_produce', 'To Produce'),], 'Requirement Type', required=True, readonly=False,),

        'qty': fields.integer('Quantity', required=True, help="Quantity"),



        'fdstage_id': fields.many2one('fdstage', 'Design Stage', select=True),



        #-- if unit of measuamentr not blank or circulation



        #'to_consume': fields.many2one('fdstage', 'Design Stage', select=True),

        #'to_produce': fields.many2one('fdstage', 'Design Stage', select=True),

        }


#def onchange_product_id(self, cr, uid, ids, link_product, name, context=None):
#    """ Changes UoM and name if product_id changes.
#    @param name: Name of the field
#    @param product_id: Changed product_id
#    @return:  Dictionary of changed values
#    """
#    if link_product:
#        prod = self.pool.get('product.product').browse(cr, uid, link_product, context=context)
#        return {'value': {'name': prod.name, 'product_uom': prod.uom_id.id}}
#    return {}


    def onchange_product_id(self, cr, uid, ids, link_product, name, context=None):
        """ Changes UoM product_id changes.
        @param link_product: Changed product_id
        @return:  Dictionary of changed values
        """
        if link_product:
            prod = self.pool.get('product.product').browse(cr, uid, link_product, context=context)
            return {'value': {'product_uom': prod.uom_id.id}}
        return {}

    def onchange_uom(self, cr, uid, ids, link_product, product_uom, context=None):
        res = {'value':{}}
        if not product_uom or not link_product:
            return res
        product = self.pool.get('product.product').browse(cr, uid, link_product, context=context)
        uom = self.pool.get('product.uom').browse(cr, uid, product_uom, context=context)
        if uom.category_id.id != product.uom_id.category_id.id:
            res['warning'] = {'title': _('Warning'), 'message': _('The Product Unit of Measure you chose has a different category than in the product form.')}
            res['value'].update({'product_uom': product.uom_id.id})
        return res


fdstage_lines()