# -*- coding: utf-8 -*-
from osv import fields, osv

import logging
from openerp.tools.translate import _
#import time
#import datetime

_logger = logging.getLogger(__name__)

class product_product(osv.osv):
    _name = 'product.product'
    _inherit = 'product.product'
    _columns = {
# материальный тип.
        'af_material_type': fields.selection([
                                             ('Goods','Goods-Товар'),
                                             ('Productions','Productions-Продукция'),
                                             ('Fixed_Assets','Fixed Assets-Основные средства'),
                                             ('Consumable_Item','Consumable Item-Расходный материал'),
                                             ('Intangible Asset','Intangible Asset-Нематериальный актив'),
                                             ],'Мaterial Type', select=True, change_default=True),

        }

product_product()


class ext_devision(osv.osv):

    _name = 'ext.devision'
    _description = "Devision"

    _columns = {

        'name': fields.char('Devision Name', size=128, required=False),
        'description': fields.text('Description'),



        # Conect to fabric design # FIXME dsd

        #'fdesign_id': fields.many2one('fdesign', 'Fabric design', select=True),
        #'fdstage_lines_ids': fields.one2many('fdstage.lines', 'fdstage_id', 'Stage Lines'),

        }

ext_devision()




