# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2012 ITS-1 (<http://www.its1.lv/>)
#                       E-mail: <info@its1.lv>
#                       Address: <Vienibas gatve 109 LV-1058 Riga Latvia>
#                       Phone: +371 66116534
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

{
    'name': 'Latvia - Stock',
    'version': '1.0',
    'description': """
Latvian localisation for stock module.
=====================================
Adds a filter to product view, which allows to show only those products, whose quantities are greater than zero.

If supplier invoices or refunds are supposed to be created from product moves and the destination location for a certain stock move is of type 'Supplier' (for example, products are returned to supplier and a Supplier Refund is created), and the product's valuation is Real Time, the account for the invoice will be taken from the products or it's category's Stock Output Account instead of Expense Account.

Makes all picking types (not just type 'in') considered, when computing average price of the product.
    """,
    'author': 'ITS-1',
    'website': 'http://www.its1.lv/',
    'category': 'Localization/Stock',
    'depends': ['stock', 'l10n_lv_account'],
    'demo_xml': [],
    'update_xml': [
        'product_view.xml'
    ],
    'auto_install': False,
    'installable': True,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
