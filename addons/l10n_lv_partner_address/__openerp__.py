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
    'name': 'Partner - Address',
    'version': '1.0',
    'description': """
Addresses.
=====================================

Adds a new object for addresses, so you don't have to necessarily create a Partner to add an Address (but, if a Partner with address fields is created, a new Address with Partner will be created automatically, and you can edit this Address from a Partner's card or from an Address card, by choice).
Also, you can create Address Types for juridical or physical persons.

Adds Office Address and Delivery Address to a Partner, if the Partner is a Company.

Adds a new field 'Company Registry' to Partner (if it is a company).
    """,
    'author': 'ITS-1',
    'website': 'http://www.its1.lv/',
    'category': 'Hidden',
    'depends': ['base'],
    'demo_xml': [],
    'update_xml': [
        'security/ir.model.access.csv',
        'res_partner_address_view.xml',
        'res_partner_address_data.xml'
    ],
    'auto_install': False,
    'installable': True,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
