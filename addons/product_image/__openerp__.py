{
    "name" : "Product Image",
    "version" : "0.1",
    "author" : "Stefan Reisich, Rove.design GmbH",
    "website" : "http://www.rove.de/",
    "description": """
This Module overwrites openerp.web.list.Binary field to show the product image in the listview. A new column with product image is added.
    """,
    "depends" : [
                 "sale",
                 "sale_stock",
                 "stock"
    ],
    'js': [
           'static/src/js/view_list.js'
    ],
    "data": [
        'product_view.xml',
        'sale_view.xml',
        'stock_view.xml'
    ],
    'installable': True,
    "active": False,
}
