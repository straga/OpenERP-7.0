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

from openerp.osv import fields, osv
import sys
from openerp.tools.translate import _
import base64
import openerp.addons.decimal_precision as dp
import time
from datetime import datetime

class account_fidavista_export_payments(osv.osv_memory):
    _name = 'account.fidavista.export.payments'

    _columns = {
        'wizard_id': fields.many2one('account.fidavista.export', 'Wizard'),
        'payment_number': fields.char('Payment Number', size=32),
        'partner_id': fields.many2one('res.partner', 'Partner', required=True),
        'bank_account_id': fields.many2one('res.partner.bank', 'Bank Account', required=True)
    }

class account_fidavista_export(osv.osv_memory):
    _name = 'account.fidavista.export'
    _description = 'Export FiDAViSta File'

    _columns = {
        'name': fields.char('File Name', size=32),
        'period_id': fields.many2one('account.period','Period', required=True),
        'file_save': fields.binary('Save File', filters='*.xml', readonly=True),
        'partner_id': fields.many2one('res.partner', 'Related Partner'),
        'bank_account_id': fields.many2one('res.partner.bank', 'Bank Account', required=True),
        'payments_ids': fields.one2many('account.fidavista.export.payments', 'wizard_id', 'Payment Data')
    }

    def _get_period(self, cr, uid, context=None):
        if context is None:
            context = {}
        period_obj = self.pool.get('account.period')
        date = time.strftime('%Y-%m-%d')
        period_id = period_obj.search(cr, uid, [('date_start','<=',date),('date_stop','>=',date)], context=context)
        if period_id:
            return period_id[0]
        return False

    def _get_partner(self, cr, uid, context=None):
        obj_user = self.pool.get('res.users')
        partner_id = obj_user.browse(cr, uid, uid, context=context).company_id.partner_id.id or False
        return partner_id

    _defaults = {
        'name': 'FiDAViSta_export.xml',
        'period_id': _get_period,
        'partner_id': _get_partner
    }

    def onchange_period_id(self, cr, uid, ids, period_id, bank_account, context=None):
        if context is None:
            context = {}
        payment_vals = []
        bank_acc_obj = self.pool.get('res.partner.bank')
        payment_obj = self.pool.get('account.voucher')
        payment_ids = payment_obj.search(cr, uid, [('period_id','=',period_id)], context=context)
        for payment in payment_obj.browse(cr, uid, payment_ids, context=context):
            bank_account_id = False
            for bank_acc in payment.partner_id.bank_ids:
                if bank_account:
                    bank_acc_c = bank_acc_obj.browse(cr, uid, bank_account, context=context)
                    if bank_acc.bank.id == bank_acc_c.bank.id:
                        bank_account_id = bank_acc.id
                        break
                    else:
                        bank_account_id = bank_acc.id
                else:
                    bank_account_id = bank_acc.id
            payment_vals.append({'payment_number': payment.number, 'partner_id': payment.partner_id.id, 'bank_account_id': bank_account_id})
        return {'value': {'payments_ids': payment_vals}}

    def create_xml(self, cr, uid, ids, context=None):
        if context is None:
            context = {}

        data_exp = self.browse(cr, uid, ids[0])
        bank_acc_obj = self.pool.get('res.partner.bank')
        payment_obj = self.pool.get('account.voucher')
        payment_ids = payment_obj.search(cr, uid, [('period_id','=',data_exp.period_id.id)], context=context)

        data_of_file = """<?xml version="1.0" encoding="UTF-8" ?>
<FIDAVISTA xmlns="http://bankasoc.lv/fidavista/fidavista0101.xsd">"""
        data_of_file += "\n    <Header>"
        data_of_file += ("\n        <Timestamp>" + datetime.now().strftime('%Y%m%d%H%M%S%f')[:-3] + "</Timestamp>")
        company = self.pool.get('res.users').browse(cr, uid, uid, context=context).company_id
        data_of_file += ("\n        <From>" + company.name + "</From>")
        data_of_file += "\n    </Header>"

        for payment in payment_obj.browse(cr, uid, payment_ids, context=context):
            data_of_file += "\n    <Payment>"
            if payment.reference:
                data_of_file += ("\n        <ExtId>" + payment.reference + "</ExtId>")
            data_of_file += ("\n        <DocNo>" + payment.number + "</DocNo>")
            data_of_file += ("\n        <RegDate>" + payment.date + "</RegDate>")
            data_of_file += ("\n        <TaxPmtFlg>" + "N" + "</TaxPmtFlg>")
            data_of_file += ("\n        <Ccy>" + payment.payment_rate_currency_id.name + "</Ccy>")
            note = payment.narration
            if not note:
                note = payment.partner_id.name + " " + payment.number
            data_of_file += ("\n        <PmtInfo>" + note + "</PmtInfo>")
            if company.company_registry:
                data_of_file += ("\n        <PayLegalId>" + company.company_registry + "</PayLegalId>")
            data_of_file += ("\n        <PayAccNo>" + (data_exp.bank_account_id.acc_number).replace(" ","") + "</PayAccNo>")
            if payment.currency_id:
                data_of_file += ("\n        <DebitCcy>" + payment.currency_id.name + "</DebitCcy>")
            data_of_file += ("\n        <BenSet>")
            data_of_file += ("\n            <BenExtId>" + str(payment.partner_id.id) + "</BenExtId>")
            data_of_file += ("\n            <Priority>" + "N" + "</Priority>")
            comm = "SHA"
            if (payment.currency_id) and (payment.currency_id.id != payment.payment_rate_currency_id.id):
                comm = "OUR"
            if (not payment.currency_id) and (company.currency_id.id != payment.payment_rate_currency_id.id):
                comm = "OUR"
            data_of_file += ("\n            <Comm>" + comm + "</Comm>")
            data_of_file += ("\n            <Amt>") + str(payment.amount) + ("</Amt>")
            bank_acc_no = False
            bank_acc = False
            for wiz_payment in data_exp.payments_ids:
                if payment.number == wiz_payment.payment_number:
                    bank_acc = wiz_payment.bank_account_id
                    bank_acc_no = (bank_acc.acc_number).replace(" ","")
                    break
            data_of_file += ("\n            <BenAccNo>" + bank_acc_no + "</BenAccNo>")
            flg = "N"
            if bank_acc.state == 'iban':
                flg = "Y"
            data_of_file += ("\n            <BenAccIbanFlg>" + flg + "</BenAccIbanFlg>")
            data_of_file += ("\n            <BenName>" + payment.partner_id.name + "</BenName>")
            vat = payment.partner_id.company_registry
            if (not vat) and (payment.partner_id.vat):
                vat = ((payment.partner_id.vat).replace(" ","").upper())[2:]
            if vat:
                data_of_file += ("\n            <BenLegalId>" + vat + "</BenLegalId>")
            address = ""
            city = payment.partner_id.city
            if city:
                address += city
            street = payment.partner_id.street
            if street:
                if payment.partner_id.street2:
                    street = street + " " + payment.partner_id.street2
                if city:
                    address += " "
                address += street
            zip = payment.partner_id.zip
            if zip:
                if city or street:
                    address += ", "
                address += zip
            if address != "":
                data_of_file += ("\n            <BenAddress>" + address + "</BenAddress>")
            country_code = False
            if payment.partner_id.country_id:
                country_code = payment.partner_id.country_id.code
                if (not country_code) and payment.partner_id.vat:
                    country_code = (payment.partner_id.vat).upper()[:2]
            if country_code:
                data_of_file += ("\n            <BenCountry>" + country_code + "</BenCountry>")
            if not country_code:
                raise osv.except_osv(_('Insufficient data!'), _('No Country or VAT defined for Partner "%s", but the Country Code is a mandatory tag. Please define either a Country or a VAT to get the Country Code!') % (payment.partner_id.name))
            bank_name = bank_acc.bank_name or (bank_acc.bank and bank_acc.bank.name) or False
            if bank_name:
                data_of_file += ("\n            <BBName>" + bank_name + "</BBName>")
            if bank_acc.bank:
                bank_address = ""
                b_city = bank_acc.bank.city
                if b_city:
                    bank_address += b_city
                b_street = bank_acc.bank.street
                if b_street:
                    if bank_acc.bank.street2:
                        b_street = b_street + " " + bank_acc.bank.street2
                    if b_city:
                        bank_address += " "
                    bank_address += b_street
                b_zip = bank_acc.bank.zip
                if b_zip:
                    if b_city or b_street:
                        bank_address += ", "
                    bank_address += b_zip
                if bank_address != "":
                    data_of_file += ("\n            <BBAddress>" + bank_address + "</BBAddress>")
            swift = bank_acc.bank_bic or (bank_acc.bank and bank_acc.bank.bic) or False
            if swift:
                data_of_file += ("\n            <BBSwift>" + swift + "</BBSwift>")
            data_of_file += ("\n        </BenSet>")
            data_of_file += "\n    </Payment>"

        data_of_file += "\n</FIDAVISTA>"

        data_of_file_real = base64.encodestring(data_of_file.encode('utf8'))
        self.write(cr, uid, ids, {'file_save': data_of_file_real, 'name': data_exp.name}, context=context)

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'account.fidavista.export',
            'view_type': 'form',
            'view_mode': 'form',
            'res_id': data_exp.id,
            'views': [(False,'form')],
            'target': 'new',
        }


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
