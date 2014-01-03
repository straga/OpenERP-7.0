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

import math

from osv import fields,osv
import tools
import pooler
from tools.translate import _

class res_partner_address_type(osv.osv):
    _description ='Partner Address Types'
    _name = 'res.partner.address.type'

    _columns = {
        'name': fields.char('Type Name', size=36, required=True),
        'for': fields.selection([('juridical','Juridical Person'),('physical','Physical Person')], 'For', required=True, help="Choose the type of person this address type will be used for.")
    }

res_partner_address_type()

class res_partner_address(osv.osv):
    _description ='Partner Addresses'
    _name = 'res.partner.address'
    _order = 'type, street'
    _rec_name = 'street'

    _columns = {
        'partner_id': fields.many2one('res.partner', 'Partner', ondelete='cascade'),
        'type': fields.many2one('res.partner.address.type', 'Type'),
        'street': fields.char('Street', size=256),
        'zip': fields.char('Zip', change_default=True, size=24),
        'city': fields.char('City', size=128),
        'state_id': fields.many2one("res.country.state", 'Fed. State', domain="[('country_id','=',country_id)]"),
        'country_id': fields.many2one('res.country', 'Country'),
        'is_customer_add': fields.related('partner_id', 'customer', type='boolean', string='Customer'),
        'is_supplier_add': fields.related('partner_id', 'supplier', type='boolean', string='Supplier'),
        'active': fields.boolean('Active', help="Uncheck the active field to hide the contact."),
        'company_id': fields.many2one('res.company', 'Company',select=1),
        'color': fields.integer('Color Index'),
        'partner_street': fields.related('partner_id', 'street', type='char', string='Partner Street'),
        'partner_street2': fields.related('partner_id', 'street2', type='char', string='Partner Street 2'),
        'partner_city': fields.related('partner_id', 'city', type='char', string='Partner City'),
        'partner_zip': fields.related('partner_id', 'zip', type='char', string='Partner Zip'),
        'partner_state': fields.related('partner_id', 'state_id', type='many2one', relation='res.country.state', string='Partner State'),
        'partner_country': fields.related('partner_id', 'country_id', type='many2one', relation='res.country', string='Partner Country'),
        'for_domain1': fields.char('For Domain 1', size=16),
        'for_domain2': fields.char('For Domain 2', size=16),
    }

    def _get_default_country(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        company_obj = self.pool.get('res.company')
        company_id = company_obj._company_default_get(cr, uid, 'res.partner.address', context=context)
        country_id = company_obj.browse(cr, uid, company_id, context=context).partner_id.country_id.id or ''
        return country_id

    _defaults = {
        'active': lambda *a: 1,
        'company_id': lambda s,cr,uid,c: s.pool.get('res.company')._company_default_get(cr, uid, 'res.partner.address', context=c),
        'country_id': _get_default_country,
        'for_domain1': 'juridical',
        'for_domain2': 'physical'
    }

    def name_get(self, cr, user, ids, context=None):
        if context is None:
            context = {}
        if not len(ids):
            return []
        res = []
        for r in self.read(cr, user, ids, ['street','city','zip','country_id']):
            # make a comma-separated list with the following non-empty elements
            elems = [r['street'], r['city'], r['zip']]
            addr = ', '.join(filter(bool, elems))
            res.append((r['id'], addr or '/'))
        return res

    def onchange_street(self, cr, uid, ids, street, partner_id, context=None):
        if context is None:
            context = {}
        if partner_id:
            return {'value': {'partner_street': street, 'partner_street2': False}}
        return {}

    def onchange_city(self, cr, uid, ids, city, partner_id, context=None):
        if context is None:
            context = {}
        if partner_id:
            return {'value': {'partner_city': city}}
        return {}

    def onchange_zip(self, cr, uid, ids, zip, partner_id, context=None):
        if context is None:
            context = {}
        if partner_id:
            return {'value': {'partner_zip': zip}}
        return {}

    def onchange_state_id(self, cr, uid, ids, state_id, partner_id, context=None):
        if context is None:
            context = {}
        if partner_id:
            return {'value': {'partner_state': state_id}}
        return {}

    def onchange_country_id(self, cr, uid, ids, country_id, partner_id, context=None):
        if context is None:
            context = {}
        domain = {}
        if country_id:
            domain = {'state_id': [('country_id', '=', country_id)]}
        if partner_id:
            return {'value': {'partner_country': country_id}, 'domain': domain}
        return {'domain': domain}

res_partner_address()

class res_partner(osv.osv):
    _inherit = "res.partner"
    _columns = {
        'company_registry': fields.char('Company Registry', size=64),
        'address_id': fields.one2many('res.partner.address', 'partner_id', 'Address'),
        'office_address': fields.many2one('res.partner.address', 'Office Address', help='Enter this address, if it differs from Legal Address.'),
        'delivery_address': fields.many2one('res.partner.address', 'Delivery Address', help='Enter this address, if it differs from Legal Address.')
    }

    def _create_address(self, cr, uid, record, context=None):
        if context is None:
            context = {}
        address_obj = self.pool.get('res.partner.address')
        address_type_obj = self.pool.get('res.partner.address.type')
        address_type_physical = address_type_obj.search(cr, uid, [('for','=','physical')], context=context)[0]
        address_type_juridical = address_type_obj.search(cr, uid, [('for','=','juridical')], context=context)[0]
        street = record.street
        if street and record.street2:
            street = record.street + ' ' + record.street2
        state = record.state_id and record.state_id.id or ''
        country = record.country_id and record.country_id.id or ''
        address_id = []
        for addr in record.address_id:
            address_id.append((addr.id))
        if address_id:
            address = address_obj.browse(cr, uid, address_id[0], context=context)
            address_state = address.state_id and address.state_id.id or ''
            address_country = address.country_id and address.country_id.id or ''
            if address.street != street:
                address_obj.write(cr, uid, address.id, {'street': street}, context=context)
            if address.city != record.city:
                address_obj.write(cr, uid, address.id, {'city': record.city}, context=context)
            if address.zip != record.zip:
                address_obj.write(cr, uid, address.id, {'zip': record.zip}, context=context)
            if address_state != state:
                address_obj.write(cr, uid, address.id, {'state_id': state}, context=context)
            if address_country != country:
                address_obj.write(cr, uid, address.id, {'country_id': country}, context=context)
            if record.is_company == True:
                address_obj.write(cr, uid, address.id, {'type': address_type_juridical, 'for_domain1': 'juridical', 'for_domain2': 'juridical'}, context=context)
            if record.is_company == False:
                address_obj.write(cr, uid, address.id, {'type': address_type_physical, 'for_domain1': 'physical', 'for_domain2': 'physical'}, context=context)
        if (not address_id) and (street or record.city or record.zip or record.state_id or record.country_id):
            if record.is_company == True:
                addr_type = address_type_juridical
                for_domain1 = 'juridical'
                for_domain2 = 'juridical'
            if record.is_company == False:
                addr_type = address_type_physical
                for_domain1 = 'physical'
                for_domain2 = 'physical'
            address_obj.create(cr, uid, {'partner_id': record.id, 'street': street, 'city': record.city, 'zip': record.zip, 'state_id': state, 'country_id': country, 'type': addr_type, 'for_domain1': for_domain1, 'for_domain2': for_domain2}, context=context)
        return True


    def write(self, cr, uid, ids, vals, context=None):
        if context is None:
            context = {}
        res = super(res_partner, self).write(cr, uid, ids, vals, context=context)
        if isinstance(ids, list):
            ids = ids
        else:
            ids = [int(ids)]
        for record in self.browse(cr, uid, ids, context=context):
            self._create_address(cr, uid, record, context=context)
        return res

res_partner()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
