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
    'name': 'Latvia - Employee Directory',
    'version': '1.0',
    'description': """
Latvian localisation for hr module.
=====================================

Field Home Address changed to Declared Address.
New field Residence Address added.
All address fields changed to res.partner.address.
New fields for passport added: Passport Issue Date and Passport Expiration Date.
New fields for Additional Information added: Contract, Contract Start Date and Introductory Done
Settings -> Configuration -> Human Resources: Personal Information: Use employee name and surname in separate fields.
Settings -> Configuration -> Human Resources: Curriculum Vitae: Use employees CV text.

Addtional fields for Contracts: Main Duties, Additional Duties, Other Terms.

Report for Contracts: Employee Contract - prints out a contract to sign.

Removes User simple view, so that new users (with default name) can be created from employees.
    """,
    'author': 'ITS-1',
    'website': 'http://www.its1.lv/',
    'category': 'Localization/Human Resources',
    'depends': ['hr_contract', 'report_webkit', 'l10n_lv_partner_address', 'portal_hr_employees'],
    'demo_xml': [],
    'update_xml': [
        'security/hr_security.xml',
        'security/ir.model.access.csv',
        'res_company_view.xml',
        'hr_view.xml',
        'hr_report.xml'
    ],
    'auto_install': False,
    'installable': True,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
