
from osv import fields, osv

class ampf_productsize(osv.osv):
    _name = 'ampf.productsize'
    _columns = {
        'name': fields.char('Name', size=20),
        'ampf_productsize_id': fields.many2one('product.product', 'Id', required=True, ondelete='cascade'),
        'ampf_productsize_diametr': fields.float('Diametr', digits=(10,2)),
        'ampf_productsize_width': fields.float('Width', digits=(10,2)),
        'ampf_productsize_lenght': fields.float('Lenght', digits=(10,2)),
        'ampf_productsize_height': fields.float('Height', digits=(10,2)),
        'ampf_productsize_windows': fields.float('Windows', digits=(10,2)),
        'ampf_productsize_windows_diametr': fields.float('Windows Diametr', digits=(10,2)),
    }
ampf_productsize()

class product_product(osv.osv):
    _name = 'product.product'
    _inherit = 'product.product'
    _columns = {
        'ampf_productsize_ids': fields.one2many('ampf.productsize', 'ampf_productsize_id', 'ProductSize'),
    }
product_product()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: