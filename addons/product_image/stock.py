from openerp.osv import fields, osv

class stock_move(osv.Model):
    _name = 'stock.move'
    _inherit = 'stock.move'

    def onchange_product_id(self, cr, uid, ids, prod_id=False, loc_id=False,
                            loc_dest_id=False, partner_id=False):
        res_prod = super(stock_move, self).onchange_product_id(cr, uid, ids, prod_id, loc_id,loc_dest_id, partner_id)
        prod_obj = self.pool.get('product.product')
        obj = prod_obj.browse(cr, uid, prod_id)
        res_prod['value'].update({'image_small': obj.image_small})
        return res_prod


    _columns = {
        'image_small' : fields.binary('Product Image'),
    }

stock_move()

class sale_order_line(osv.Model):
    _name = 'sale.order.line'
    _inherit = 'sale.order.line'
    _columns = {
        'image_small' : fields.binary('Product Image'),
    }

    def product_id_change(self, cr, uid, ids, pricelist, product, qty=0,
                          uom=False, qty_uos=0, uos=False, name='', partner_id=False,
                          lang=False, update_tax=True, date_order=False, packaging=False, fiscal_position=False, flag=False,image_small=False, context=None):
        context = context or {}

        res = super(sale_order_line, self).product_id_change(cr, uid, ids, pricelist, product, qty=qty,
                                                             uom=uom, qty_uos=qty_uos, uos=uos, name=name, partner_id=partner_id,
                                                             lang=lang, update_tax=update_tax, date_order=date_order, packaging=packaging, fiscal_position=fiscal_position, flag=flag, context=context)

        product_obj = self.pool.get('product.product')
        product_obj = product_obj.browse(cr, uid, product, context=context)

        res['value'].update({'image_small': product_obj.image_small or False})
        return res


sale_order_line()

class sale_order(osv.Model):
    _name = 'sale.order'
    _inherit = 'sale.order'

    def _prepare_order_line_move(self, cr, uid, order, line, picking_id, date_planned, context=None):
        res = super(sale_order, self)._prepare_order_line_move(cr, uid, order=order, line=line, picking_id=picking_id, date_planned=date_planned, context=context)
        res['image_small'] = line.image_small
        return res

sale_order()
