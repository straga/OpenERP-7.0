# -*- coding: utf-8 -*-
#from osv import fields, osv

import math
import re
import logging
import openerp.addons.decimal_precision as dp

#from _common import rounding
from openerp import tools
from openerp.osv import osv, fields
from openerp.tools.translate import _


_logger = logging.getLogger(__name__) # Need for message in console.

class product_product(osv.osv):
    _name = 'product.product'
    _inherit = 'product.product'

    def button_price_rule(self, cr, uid, ids, context=None): #button action for mass add.

        prod_id = int(''.join(map(str,ids)))    # list to int

        context = context or {}
        _logger.warning("Context = %s", context)

        #_logger.warning("IDS = %s", prod_id )   #log in sonsole

        if ids:
                prod = self.pool.get('product.template').browse(cr, uid, prod_id, context=context)

                # from product with product id.
                #prod = self.pool.get('product.template').browse(cr, uid, 8) for example with id 8
                #Return many values
                #return {'value': {'name': prod.name, 'product_uom': prod.uom_id.id}}


                _logger.warning("UOM = %s", prod.uom_id) #get name Unit of mesaumetr
                _logger.warning("UOM_id = %s", prod.uom_id.id) #get id Unit of mesaumetr


                # Select max seq from circulation for fabric.main. it be max 3. it mean 3 sales quatation.
                #cr.execute('select MAX(circulation_seq) from fabric_circulation where fabric_id=%s', (fabric_id,))
                #seq_list = map(lambda x: x[0], cr.fetchall()) # convert from [2,] to [2]


                # It can Direct make product in Price item
                # idea_id = self.pool.get('product.pricelist.item').create(cr, uid,
                #                       { 'name': 'Spam recipe',
                #                         'product_id': prod_id,
                #                         'min_quantity' : 16000,
                #                         'sequence': 45,
                #                         'price_version_id': 5,
                #                         'base': 1,
                #                         'price_surcharge': 0.55,
                #
                #
                #                         })

                try:
                    # Execute the SQL command
                    type_opt = 'circulation'
                    cr.execute('select id_opt AS oid , name_opt AS oname from res_extended where type_opt=%s order by 1', (type_opt,))
                    data = cr.dictfetchall()

                    #_logger.warning("data = %s", data)
                    #fields = []



                    for rec in data:
                        #fields['id_opt'] = rec.get('id_opt')
                        #fields['name_opt'] = rec.get('name_opt')

                        oid = rec.get('oid')
                        oname = rec.get('oname','')



                        _logger.warning("id_opt = %s", oid)
                        _logger.warning("name_opt = %s", oname)

                        #if dprice_version_id:
                        #    _logger.warning("name_opt = %s", oname)

                            # It can Direct make product in Price item
                            # idea_id = self.pool.get('product.pricelist.item').create(cr, uid,
                            #            {
                            #             'name': 'Spam recipe',
                            #             'product_id': prod_id,
                            #             'min_quantity' : oname,
                            #             'sequence': oid,
                            #             'price_version_id': 5,
                            #             'base': 1,
                            #             'price_surcharge': 0.00,
                            #              })




                except:
                    return False


                #_logger.warning("cir_list = %s", cir_list)
                #cir_list2 = map(lambda x: x[0], cir_list) # convert from [2,] to [2]
                #_logger.warning("cir_list2 = %s", cir_list2)

        return True


    _columns = {
        # For display price in product.
        'prices_ids': fields.one2many('product.pricelist.item', 'product_id', 'Supplier'),
       }


product_product()


class product_pricelist_item(osv.osv):
    _name = 'product.pricelist.item'
    _inherit = 'product.pricelist.item'
    _columns = {


        }

product_pricelist_item()



# for store more option in res.extended. It for store in one place any options.
class res_extended(osv.osv):
    _name = 'res.extended'

    _columns = {

        'type_opt': fields.char('Type Name', size=128, required=False),
        'id_opt': fields.integer('Id Opt.', required=False, help="Id opt"),
        'name_opt': fields.char('Type Name', size=128, required=False),
        'value_opt': fields.char('Type Name', size=128, required=False),

    }

res_extended()







