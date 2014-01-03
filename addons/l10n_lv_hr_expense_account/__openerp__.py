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
    'name': 'Latvian Localization for Expense Management - Accounting',
    'version': '1.0',
    'category': 'Human Resources',
    'description': """
Latvian localization for hr_expense_account module.
==========================================================
    """,
    'author': 'ITS-1',
    'website': 'http://www.its1.lv/',
    'depends': ['hr_expense_account', 'l10n_lv_report_webkit', 'account_sequence'],
    'init_xml': [],
    'demo_xml': [],
    'update_xml': [
        'hr_expense_account_report.xml',
        'wizard/hr_expense_account_report_view.xml'
    ],
    'installable': True,
    'auto_install': False
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
