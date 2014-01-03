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
    'name': 'Latvian Localization for Bank Statement data importation',
    'version': '1.0',
    'description': """
Latvian localization, which allows data import from bank export in FiDAViSta format.
=====================================
Accounting (Invoicing) -> Bank and Cash -> Import FiDAViSta File: select an .xml file to import in the system; shows and compares the balances of prevoiusly imported statements and the statements you are about to import; creates Bank Statements (each for every Bank Account).

Accounting (Invoicing) -> Configuration -> FiDAViSta -> Transaction Types: create a transaction type configuration in order to get Accounts for Bank Statement Lines (form <TypeCode> or <TypeName> tags (if <TypeCode> is not present)).

A new field Partner Name has been added to Bank Statement Lines, it (as well as other data from the FiDAViSta file) will be used as default, when you try to create a new Partner from a Bank Statement Line.

Adds default Receivable and Payable accounts to a Partner and a restriction to create Partner's Bank Accounts: you can only create them, if the Partner has been saved.

Adds a menu to Accounting (Invoicing) -> Configuration: Finances -> Banks, where you have already imported banks from this module and also the opportunity to create new ones.
    """,
    'author': 'ITS-1',
    'website': 'http://www.its1.lv/',
    'category': 'Localization',
    'depends': ['l10n_lv_account', 'l10n_lv', 'account_payment'],
    'init_xml': [],
    'demo_xml': [],
    'update_xml': [
        'security/ir.model.access.csv',
        'res.bank.csv',
        'wizard/wizard_fidavista_config_view.xml',
        'account_bank_statement_view.xml',
        'account_fidavista_config_view.xml',
        'wizard/account_fidavista_import_view.xml',
        'wizard/account_fidavista_export_view.xml',
        'res_partner_view.xml',
        'res_bank_view.xml'
        ],
    'auto_install': False,
    'installable': True,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
