# -*- coding: utf-8 -*-
from osv import fields, osv

import logging
from openerp.tools.translate import _
from operator import itemgetter
#import time
#import datetime

_logger = logging.getLogger(__name__)


def check_cycle(self, cr, uid, ids, context=None):
    """ climbs the ``self._table.parent_id`` chains for 100 levels or
    until it can't find any more parent(s)

    Returns true if it runs out of parents (no cycle), false if
    it can recurse 100 times without ending all chains
    """
    level = 100
    while len(ids):
        cr.execute('SELECT DISTINCT parent_id ' \
                   'FROM '+self._table+' ' \
                                       'WHERE id IN %s ' \
                                       'AND parent_id IS NOT NULL',(tuple(ids),))
        ids = map(itemgetter(0), cr.fetchall())
        if not level:
            return False
        level -= 1
    return True


#Параметры Конструкции.
class fdesign(osv.osv):

    _name = 'fdesign'
    _description = "Fabric Design"

    _order = "parent_left"
    _parent_order = "parent_left"
    _parent_store = True

    def _get_children_and_consol(self, cr, uid, ids, context=None):
        #this function search for all the children and all consolidated children (recursively) of the given account ids
        ids2 = self.search(cr, uid, [('parent_id', 'child_of', ids)], context=context)
        ids3 = []
        for rec in self.browse(cr, uid, ids2, context=context):
            for child in rec.child_consol_ids:
                ids3.append(child.id)
        if ids3:
            ids3 = self._get_children_and_consol(cr, uid, ids3, context)

        _logger.error("_get_children_and_consol %s", ids2 + ids3)

        return ids2 + ids3

    def _get_child_ids(self, cr, uid, ids, field_name, arg, context=None):
        result = {}
        for record in self.browse(cr, uid, ids, context=context):
            if record.child_parent_ids:
                result[record.id] = [x.id for x in record.child_parent_ids]
            else:
                result[record.id] = []

            if record.child_consol_ids:
                for acc in record.child_consol_ids:
                    if acc.id not in result[record.id]:
                        result[record.id].append(acc.id)

        _logger.error("RRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRR %s", result)

        return result

    def _get_level(self, cr, uid, ids, field_name, arg, context=None):
        res = {}

        #_logger.error("1 _get_level %s", res)

        for fdesign in self.browse(cr, uid, ids, context=context):
            #we may not know the level of the parent at the time of computation, so we
            # can't simply do res[account.id] = account.parent_id.level + 1
            level = 0
            parent = fdesign.parent_id
            while parent:
                level += 1
                parent = parent.parent_id
            res[fdesign.id] = level

        #_logger.error("2 _get_level %s", res)

        return res

    _columns = {

        'id_design': fields.char('ID design', size=15, required=True),
        'name': fields.char('Design Name', size=128, required=True),
        'description': fields.text('Description'),
        #'link_product': fields.many2one('product.product', 'Link Product', change_default=True, select=True),
        #'product_uom': fields.many2one('product.uom', 'Product Unit of Measure', required=False, help="Unit of Measure (Unit of Measure) is the unit of measurement for the inventory control"),


        #psize габариты продукта
        'psize_h': fields.integer('p size H', required=True, help="Size H for new fabrik design product"),
        'psize_w': fields.integer('p size W', required=True, help="Size W for new fabrik design product"),
        'psize_z': fields.integer('p size Z', required=True, help="Size Z for new fabrik design product"),

        #развёртка изделия - unfolding
        'a_pknsize_h': fields.integer('a pkn size H', required=True, help="Size H for unfolding product"),
        'a_pknsize_w': fields.integer('a pkn size W', required=True, help="Size W for unfolding product"),

        #заготовка для развёртки
        'b_blanksize_h': fields.integer('a blank size H', required=True, help="Size H for blank unfolding"),
        'b_blanksize_w': fields.integer('a blank size W', required=True, help="Size W for blank unfolding"),

        #изделий на заготовке
        'qty_onblank_b': fields.integer('qty on blank', required=True, help="Qty. product on blank"),

        #blade	ножей для формы	в метрах
        'blade': fields.integer('blade', required=True, help=" blade "),
        'state': fields.selection([('cancel', 'Cancelled'),('draft', 'Draft'),('confirmed', 'Confirmed'),('exception', 'Exception'),('done', 'Done')], 'Status', required=True, readonly=True,),

        #conect fabric project - change to many2many
        'link_fabric_id': fields.many2one('fabric', 'Fabric Main', select=True),

        # Link circulation for design
        'link_fdesign_circulation': fields.one2many('fdesign.circulation', 'fdesign_id', 'Design Circulation'),

        'link_fdstage': fields.one2many('fdstage', 'fdesign_id', 'Design Stage'),


        #tree view

        #'parent_id': fields.many2one('account.account', 'Parent', ondelete='cascade', domain=[('type','=','view')]) domain=[('link_fabric_id','=','view')],
        'parent_id': fields.many2one('fdesign', 'Parent', ondelete='cascade', ),

        'child_parent_ids': fields.one2many('fdesign','parent_id','Children'),

        'child_id': fields.function(_get_child_ids, type='many2many', relation="fdesign", string="Child"),

        'child_consol_ids': fields.many2many('fdesign', 'fdesign_consol_rel', 'child_id', 'parent_id', 'Consolidated Children'),

        'parent_left': fields.integer('Parent Left', select=1),
        'parent_right': fields.integer('Parent Right', select=1),

        'level': fields.function(_get_level, string='Level', method=True, type='integer',
                                 store={
                                     'fdesign': (_get_children_and_consol, ['level', 'parent_id'], 10),
                                     }),


        }

    _defaults = {

        'state': 'draft',

        }


    def _check_recursion(self, cr, uid, ids, context=None):
        obj_self = self.browse(cr, uid, ids[0], context=context)
        p_id = obj_self.parent_id and obj_self.parent_id.id
        if (obj_self in obj_self.child_consol_ids) or (p_id and (p_id is obj_self.id)):
            return False
        while(ids):
            cr.execute('SELECT DISTINCT child_id ' \
                       'FROM fdesign_consol_rel ' \
                       'WHERE parent_id IN %s', (tuple(ids),))
            child_ids = map(itemgetter(0), cr.fetchall())
            c_ids = child_ids
            if (p_id and (p_id in c_ids)) or (obj_self.id in c_ids):
                return False
            while len(c_ids):
                s_ids = self.search(cr, uid, [('parent_id', 'in', c_ids)])
                if p_id and (p_id in s_ids):
                    return False
                c_ids = s_ids
            ids = child_ids
        return True

    _constraints = [
        (_check_recursion, 'Error!\nYou cannot create recursive accounts.', ['parent_id']),]



    # def onchange_product_id(self, cr, uid, ids, link_product, name, context=None):
    #     """ Changes UoM product_id changes.
    #     @param link_product: Changed product_id
    #     @return:  Dictionary of changed values
    #     """
    #     if link_product:
    #         prod = self.pool.get('product.product').browse(cr, uid, link_product, context=context)
    #         return {'value': {'product_uom': prod.uom_id.id}}
    #     return {}
    #
    # def onchange_uom(self, cr, uid, ids, link_product, product_uom, context=None):
    #     res = {'value':{}}
    #     if not product_uom or not link_product:
    #         return res
    #     product = self.pool.get('product.product').browse(cr, uid, link_product, context=context)
    #     uom = self.pool.get('product.uom').browse(cr, uid, product_uom, context=context)
    #     if uom.category_id.id != product.uom_id.category_id.id:
    #         res['warning'] = {'title': _('Warning'), 'message': _('The Product Unit of Measure you chose has a different category than in the product form.')}
    #         res['value'].update({'product_uom': product.uom_id.id})
    #     return res



fdesign()


##-------------- many2many Didirectional for Main Project and Design.

##-----2--------
# Паказывает ссылки в конструкции,  в каких проектах используется.
# class fdesign(osv.osv):
#     _inherit = 'fdesign'
#     _columns = {
#         'link_fabric': fields.many2many(
#             'fabric',
#             'fabric_fdesign_rel',
#             'design_id',
#             'fabric_id',
#             'Fabric Project'),
#         }
# fdesign()


#Параменры тиража для конструкции.
class fdesign_circulation(osv.osv):

    _name = 'fdesign.circulation'
    _description = "Design Circulation"

    _columns = {

        'name': fields.char('Fabric Name', size=128, required=False),
        'description': fields.text('Description'),
        'fdesign_id': fields.many2one('fdesign', 'Id', select=True),
        'circulation_seq': fields.integer('Sequence', required=True, help="Sequence"),
        'circulation_qty': fields.integer('Quantity', required=True, help="Pre Quantity circulation "),
        'qty_onblank_b': fields.integer('qty on blank', required=True, help="Qty. product on blank"),
        'blank_qty': fields.integer('Quantity', required=True, help="Quantity blanks "),
        'waste': fields.integer('Waste', required=True, help="Quantity waste(приладка) "),
        'blank_total': fields.integer('Quantity', required=True, help="Quantity blanks total "),


        }

    _defaults = {
        'circulation_seq': lambda *a: 1,
    }

fdesign_circulation()

