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
    'name': 'Latvian Localization for Account',
    'version': '1.0',
    'description': """
Latvian localization for account module.
=====================================

Adds Invoice Address and Contact Address to all the invoices.

Report named "Invoice html" added to all Invoices and Refunds. 

Report named "Cash Book" added to Invoicing (Accounting) -> Bank and Cash -> Cash Registers, which prints out the information about the Cash Register and all its Orders.

Wizard named "Print an Order from Cash Register" added to Invoicing (Accounting) -> Bank and Cash -> Cash Registers, where you can choose a particular Cash Book Line (or several of them) and print an Order for it (them).

Invoicing (Accounting) -> Reporting -> Legal Reports -> Accounting Reports -> Chart of Accounts: calls a wizard, where you can choose a particular Chart of Accounts and print out information about all Accounts, that belong to it.

Invoicing (Accounting) -> Reporting -> Generic Reporting -> Invoices -> List of Invoices: calls a wizard, where you can choose Invoice Type and print out a list of all the invoices related to the type chosen, grouped by currencies used.

Invoicing (Accounting) -> Reporting -> Legal Reports -> Accounting Reports -> Journal Items Export: calls a wizard, where you can choose specific parameters for Journal Items export in CSV or XLS format.
    """,
    'author': 'ITS-1',
    'website': 'http://www.its1.lv/',
    'category': 'Localization',
    'depends': ['account_sequence', 'l10n_lv_report_webkit', 'l10n_lv_partner_address'],
    'init_xml': [],
    'demo_xml': [],
    'update_xml': [
        'account_data.xml',
        'account_report.xml',
        'wizard/account_chart_report_view.xml',
        'wizard/account_invoice_list_report_view.xml',
        'wizard/account_cash_order_report_view.xml',
        'wizard/account_move_line_export_view.xml',
        'account_invoice_view.xml'
        ],
    'auto_install': False,
    'installable': True,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
