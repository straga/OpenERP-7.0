# -*- coding: utf-8 -*-
from osv import fields, osv


class mr_counters(osv.osv):


    _name = "mr.counters"
    _description = "Counters"
    _columns = {
        'name': fields.char('Counters Name', size=128, required=True),
        'description': fields.char('Decription'),
        'counter_type': fields.selection([
            ('water','Water Counter'),
            ('energy','Energy Counter'),
            ('LPG','LPG Counter'),
            ],'Counter Type', select=True, change_default=True),
        'link_product': fields.many2one('product.product', 'Link Product', change_default=True, select=True),
        'link_agreement': fields.many2one('sale.recurring_orders.agreement', 'Agreement', change_default=True, select=True),
        'virtual_counter': fields.boolean('It Virtual Counter', help="Determine if virtual counter "),

    }
mr_counters()



