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

from openerp import addons
import logging
from openerp.osv import fields, osv
from openerp import tools
_logger = logging.getLogger(__name__)
import time
from tools.translate import _

class hr_contract(osv.osv):
    _name = 'hr.contract'
    _inherit = 'hr.contract'

    _columns = {
        'main_duties': fields.text('Main Duties'),
        'additional_duties': fields.text('Additional Duties'),
        'other_terms': fields.text('Other Terms'),
        'employee_name': fields.related('employee_id', 'employee_name', type='char', string='Name', store=True),
        'employee_surname': fields.related('employee_id', 'employee_surname', type='char', string='Surname', store=True),
        }

    _sql_constraints = [('contract_name', 'unique(name)', 'Contract Reference must be unique!')]
    
hr_contract()

class hr_employee(osv.osv):
    _name = 'hr.employee'
    _description = 'Employee'
    _inherit = 'hr.employee'

    def onchange_employee_name_surname(self, cr, uid, ids, employee_name, employee_surname, context=None):
        if employee_name and employee_surname:
            return {'value': {'name': employee_name + ' ' + employee_surname}}
        if employee_name and not employee_surname:
            return {'value': {'name': employee_name}}
        if employee_surname and not employee_name:
            return {'value': {'name': employee_surname}}
        if not employee_name and not employee_surname:
            return {'value': {'name': False}}
        return {}

    def onchange_name(self, cr, uid, ids, name, context=None):
        if name:
            zz = name.split(' ',1)
            name1 = zz[0]
            if len(zz) > 1:
                surname1 = zz[1]
            else:
                surname1 = ''
            return {'value': {'employee_name': name1, 'employee_surname': surname1}}
        if not name:
            return {'value': {'employee_name': False, 'employee_surname': False}}
        return {}

    _columns = {
        'address_work_id': fields.many2one('res.partner.address', 'Working Address'),
        'address_declared_id': fields.many2one('res.partner.address', 'Declared Address'),
        'address_residence_id': fields.many2one('res.partner.address', 'Residence Address'),
        'employee_name': fields.char('Name', size=32),
        'employee_surname': fields.char('Surname', size=32),
        'cv_text': fields.text('CV'),
        'passport_issue_date': fields.date('Passport Issue Date'),
        'passport_expire_date': fields.date('Passport Expiration Date'),
        'introductory_done': fields.boolean('Introductory Done'),
        'contract_date_end': fields.related('contract_id', 'date_end', type='date', string='Contract End Date'),
        'contract_date_start': fields.related('contract_id', 'date_start', type='date', string='Contract Start Date'),
    }

    _sql_constraints = [('unique_employee_id', 'unique(identification_id)', 'Identification No. must be unique!')]

hr_employee()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
