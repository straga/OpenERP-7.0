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
    'name': 'Latvian Localization for Account Asset',
    'version': '1.0',
    'description': """
Latvian localization for account_asset module.
=====================================

Adds Asset Categoty field to Supplier Invoice Lines tree (list) view, which enables the creation of a new asset, when validating a Supplier Invoice, if an Asset Category is chosen.

Adds new checkbox Compute from Next Month to Asset Category and Assets, which enables the start of depreciation computation from the first day of the month, following the month of Purchase Date.

Adds columns Date Confirmed and Date Closed to Assets, which will be needed later, when computing data for reports. Date Confirmed is set automatically, when an Asset is confirmed (as the date of the current day), but Date Closed is set via a wizard, wich is called, when action Set to Close is launched.

When creating Account Moves from Depreciation Lines, the Date for the Move is first considered the Depreciation Date of the corresponding line and then, if that date cannot be found, the current date is chosen. Also, if the Asset can be closed, the Close Date should be set via a wizard.

Adds an Asset Card report to Invoicing (Accounting) -> Assets -> Assets, which prints out detailed information about the Asset.

Adds an Asset Confirmation report to Invoicing (Accounting) -> Assets -> Assets, which prints out a document, which, contains information about the Asset and places for evaluation and signatures.

Invoicing (Accounting) -> Reporting -> Assets Reports -> Account Asset Turnover: calls a wizard, in which you have to choose a period, by defining it's starting and ending Date, and then you can print out a report of total value of Assets available in the period chosen, their acquisition, depreciation and liquidation (the calculations are grouped by accounts).

Invoicing (Accounting) -> Reporting -> Assets Reports -> List of assets: calls a wizard, in which you have to choose a Date, and then you can print out a report of list of assets available in the Date chosen (the calculations are grouped by accounts).
    """,
    'author': 'ITS-1',
    'website': 'http://www.its1.lv/',
    'category': 'Localization',
    'depends': ['account_asset', 'l10n_lv_account'],
    'init_xml': [],
    'demo_xml': [],
    'update_xml': [
        'account_asset_view.xml',
        'account_asset_invoice_view.xml',
        'account_asset_report.xml',
        'wizard/account_asset_set_close_date_view.xml',
        'wizard/report_account_asset_turnover_view.xml',
        'wizard/report_account_asset_list_view.xml'
        ],
    'auto_install': False,
    'installable': True,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
