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
import xml.etree.cElementTree as ET
import sys
from openerp.tools.translate import _
import base64
import openerp.addons.decimal_precision as dp
from xml.etree import ElementTree
from cStringIO import StringIO

class l10n_lv_vat_declaration(osv.osv_memory):
    """ Vat Declaration """
    _name = "l10n_lv.vat.declaration"
    _description = "Vat Declaration"

    _columns = {
        'name': fields.char('File Name', size=32),
        'period_from': fields.many2one('account.period','Period From', required=True),
        'period_to': fields.many2one('account.period','Period To', required=True),
        'tax_code_id': fields.many2one('account.tax.code', 'Tax Code', domain=[('parent_id', '=', False)], required=True),
        'partner_id': fields.many2one('res.partner', 'Related Partner'),
        'msg': fields.text('File created', size=64, readonly=True),
        'file_save': fields.binary('Save File', filters='*.xml', readonly=True),
        'amount_overpaid': fields.float('Amount Overpaid', digits_compute=dp.get_precision('Account'), readonly=True),
        'transfer': fields.boolean('Transfer'),
        'amount_to_transfer': fields.float('Amount To Transfer', digits_compute=dp.get_precision('Account')),
        'bank_account_id': fields.many2one('res.partner.bank', 'Bank Account')
    }

    def _get_tax_code(self, cr, uid, context=None):
        obj_tax_code = self.pool.get('account.tax.code')
        obj_user = self.pool.get('res.users')
        company_id = obj_user.browse(cr, uid, uid, context=context).company_id.id
        tax_code_ids = obj_tax_code.search(cr, uid, [('company_id', '=', company_id), ('parent_id', '=', False)], context=context)
        return tax_code_ids and tax_code_ids[0] or False

    def _get_partner(self, cr, uid, context=None):
        obj_user = self.pool.get('res.users')
        partner_id = obj_user.browse(cr, uid, uid, context=context).company_id.partner_id.id or False
        return partner_id

    _defaults = {
        'msg': 'Save the File.',
        'name': 'vat_declaration.xml',
        'tax_code_id': _get_tax_code,
        'partner_id': _get_partner
    }

    def onchange_tax_code(self, cr, uid, ids, tax_code_id, context=None):
        if context is None:
            context = {}
        tax_code = self.pool.get('account.tax.code').browse(cr, uid, tax_code_id, context=context)
        partner_id = tax_code.company_id.partner_id.id or False
        return {'value': {'partner_id': partner_id}}

    def onchange_period(self, cr, uid, ids, period_from, period_to, tax_code_id, context=None):
        if context is None:
            context = {}
        obj_tax_code = self.pool.get('account.tax.code')
        obj_user = self.pool.get('res.users')
        obj_period = self.pool.get('account.period')
        tax_code = obj_tax_code.browse(cr, uid, tax_code_id, context=context)
        if tax_code_id:
            obj_company = tax_code.company_id
        else:
            obj_company = obj_user.browse(cr, uid, uid, context=context).company_id
        tax_code_ids = obj_tax_code.search(cr, uid, [('parent_id','child_of',tax_code_id), ('company_id','=',obj_company.id)], context=context)
        period_list = []
        if period_from and not period_to:
            period_list.append(period_from)
        if period_to and not period_from:
            period_list.append(period_to)
        if period_from == period_to:
            period_list.append(period_from)
        if (period_from and period_to) and (period_from != period_to):
            period_list = obj_period.build_ctx_periods(cr, uid, period_from, period_to)
        amount = 0.00
        for p in period_list:
            ctx = context.copy()
            ctx['period_id'] = p
            tax_info = obj_tax_code.read(cr, uid, tax_code_ids, ['code','sum_period'], context=ctx)
            for item in tax_info:
                if (item['code'] == '420'):
                    amount += item['sum_period']
                    break
        return {'value': {'amount_overpaid': (amount * (-1)), 'amount_to_transfer': (amount * (-1)), 'transfer': False}}

    def _check_tax_code(self, cr, uid, tax_code_id, context=None):
        if context is None:
            context = {}
        tax_code_obj = self.pool.get('account.tax.code')
        main_tax_code_id = tax_code_obj.search(cr, uid, ['|',('name','in',['APRĒĶINĀTAIS PVN (latos)','PVN SUMMA PAR SAŅEMTAJĀM PRECĒM UN PAKALPOJUMIEM (latos), no tā:']),('code','in',['250','310']),('tax_code','in',[False,'60'])], context=context)
        if main_tax_code_id:
            code_id = tax_code_obj.search(cr, uid, [('id','=',tax_code_id),('id','child_of',main_tax_code_id)], context=context)
            if code_id:
                return True
        return False

    def _check_tax_base_code(self, cr, uid, tax_base_code_id, context=None):
        if context is None:
            context = {}
        tax_code_obj = self.pool.get('account.tax.code')
        main_tax_base_code_id = tax_code_obj.search(cr, uid, ['|',('name','in',['Priekšnodokļa bāzes','KOPĒJĀ DARĪJUMU VĒRTĪBA (latos), no tās:']),('code','in',['500','100']),('tax_code','in',[False,'40'])], context=context)
        if main_tax_base_code_id:
            base_code_id = tax_code_obj.search(cr, uid, [('id','=',tax_base_code_id),('id','child_of',main_tax_base_code_id)], context=context)
            if base_code_id:
                return True
        return False

    def _process_line(self, cr, uid, line_id, context=None):
        if context is None:
            context = {}
        amount_tax = 0.0
        amount_taxed = 0.0
        amount_untaxed = 0.0
        partner_id = False
        partner_country = False
        partner_vat = False
        partner_name = False
        doc_number = False
        doc_date = False
        tax_code = False
        tax_case_code = False
        tax_code_l = False
        invoice_id = False
        for line in line_id:
            partner_id = line.partner_id.id or False
            if partner_id:
                vat_no = line.partner_id.vat
                if vat_no:
                    vat_no = vat_no.replace(' ','').upper()
                    partner_vat = vat_no[2:]
                    partner_country = vat_no[:2]
                if not vat_no:
                    partner_country = line.partner_id.country_id.code or False
                partner_name = line.partner_id.name
                partner_fpos = line.partner_id.property_account_position and line.partner_id.property_account_position.name or False
            if line.tax_code_id and self._check_tax_code(cr, uid, line.tax_code_id.id, context=context):
                amount_tax = line.debit or line.credit
                tax_code = line.tax_code_id.tax_code
                tax_case_code = line.tax_code_id.code
            if not line.tax_code_id:
                amount_taxed = line.debit or line.credit
            if line.tax_code_id and self._check_tax_base_code(cr, uid, line.tax_code_id.id, context=context):
                tax_code_l = line.tax_code_id.tax_code
            if amount_tax == 0.0:
                amount_untaxed = amount_taxed
            if (amount_tax != 0.0) and (amount_taxed != 0.0):
                amount_untaxed = amount_taxed - amount_tax
            journal_type = line.journal_id.type
            doc_number = line.move_id.name
            doc_date = line.move_id.date
            invoice_id = line.invoice.id
            if (amount_untaxed >= 1000.0) and (not partner_country):
                raise osv.except_osv(_('Insufficient data!'), _('No VAT or Country defined for Partner "%s", but Taxed Amount is greater than 1000.00. Please define either a Country or a VAT to get the Country Code!') % (partner_name))
        return {'partner_id': partner_id, 'partner_country': partner_country, 'partner_vat': partner_vat, 'partner_name': partner_name, 'partner_fpos': partner_fpos, 'journal_type': journal_type, 'amount_tax': amount_tax, 'amount_taxed': amount_taxed, 'amount_untaxed': amount_untaxed, 'doc_number': doc_number, 'doc_date': doc_date, 'tax_code': tax_code, 'tax_case_code': tax_case_code, 'tax_code_l': tax_code_l, 'invoice_id': invoice_id}

    def _process_expense(self, cr, uid, line_id, context=None):
        if context is None:
            context = {}
        amount_tax = 0.0
        amount_untaxed = 0.0
        amount_taxed = 0.0
        partner_id = False
        partner_country = False
        partner_vat = False
        partner_name = False
        doc_number = False
        doc_date = False
        tax_code = False
        tax_case_code = False
        tax_code_l = False
        invoice_id = False
        result11 = []
        result21 = []
        datas1 = {}
        for line in line_id:
            if not line.tax_code_id:
                continue
            partner_id = line.partner_id.id or False
            if partner_id:
                vat_no = line.partner_id.vat
                if vat_no:
                    vat_no = vat_no.replace(' ','').upper()
                    partner_vat = vat_no[2:]
                    partner_country = vat_no[:2]
                if not vat_no:
                    partner_country = line.partner_id.country_id.code or False
                partner_name = line.partner_id.name
                partner_fpos = line.partner_id.property_account_position and line.partner_id.property_account_position.name or False
            journal_type = line.journal_id.type
            doc_number = line.move_id.ref
            doc_date = line.move_id.date
            invoice_id = line.invoice.id
            amount_taxed = line.debit or line.credit
            if line.tax_code_id and self._check_tax_code(cr, uid, line.tax_code_id.id, context=context):
                amount_tax = line.debit or line.credit
                tax_code = line.tax_code_id.tax_code
                tax_case_code = line.tax_code_id.code
            if line.tax_code_id and self._check_tax_base_code(cr, uid, line.tax_code_id.id, context=context):
                tax_code_l = line.tax_code_id.tax_code
                amount_untaxed = line.debit or line.credit
            if datas1.get((partner_id)):
                amount_taxed += datas1[(partner_id)]['amount_taxed']
                if line.tax_code_id and self._check_tax_code(cr, uid, line.tax_code_id.id, context=context):
                    amount_tax += datas1[(partner_id)]['amount_tax']
                if line.tax_code_id and self._check_tax_base_code(cr, uid, line.tax_code_id.id, context=context):
                    amount_untaxed += datas1[(partner_id)]['amount_untaxed']
                datas1[(partner_id)].clear()
            if not datas1.get((partner_id)):
                datas1[(partner_id)] = {'partner_id': partner_id, 'partner_country': partner_country, 'partner_vat': partner_vat, 'partner_name': partner_name, 'partner_fpos': partner_fpos, 'journal_type': journal_type, 'amount_tax': amount_tax, 'amount_taxed': amount_taxed, 'amount_untaxed': amount_untaxed, 'doc_number': doc_number, 'doc_date': doc_date, 'tax_code': tax_code, 'tax_case_code': tax_case_code, 'tax_code_l': tax_code_l, 'invoice_id': invoice_id}
            result11.append(datas1[(partner_id)])

        for object in result11:
            if object != {}:
                result21.append(object)

        return result21

    def create_xml(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        # defining objects used:
        obj_tax_code = self.pool.get('account.tax.code')
        obj_acc_period = self.pool.get('account.period')
        obj_user = self.pool.get('res.users')
        obj_partner = self.pool.get('res.partner')
        mod_obj = self.pool.get('ir.model.data')
        account_move_obj = self.pool.get('account.move')
        account_move_line_obj = self.pool.get('account.move.line')

        # getting wizard data and company:
        data_tax = self.browse(cr, uid, ids[0])
        if data_tax.tax_code_id:
            obj_company = data_tax.tax_code_id.company_id
        else:
            obj_company = obj_user.browse(cr, uid, uid, context=context).company_id

        # reading data and periods:
        data  = self.read(cr, uid, ids)[0]
        period_from = obj_acc_period.browse(cr, uid, data['period_from'][0], context=context)
        period_to = obj_acc_period.browse(cr, uid, data['period_to'][0], context=context)

        # defining file content:
        data_of_file = """<?xml version="1.0"?>
<DokPVNv4 xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
    <ParskGads>%(year)s</ParskGads>""" % ({'year': str(period_to.date_stop[:4])})

        # getting info for period tags:
        starting_month = period_from.date_start[5:7]
        ending_month = period_to.date_stop[5:7]
        if starting_month == ending_month:
            data_of_file += "\n    <ParskMen>" + str(int(starting_month)) + "</ParskMen>"
        if starting_month != ending_month:
            if ((int(ending_month) - int(starting_month) + 1) == 3) and (int(starting_month) in [1,4,7,10]):
                quarter = str(((int(starting_month) - 1) / 3) + 1)
                data_of_file += "\n    <ParskCeturksnis>" + quarter + "</ParskCeturksnis>"
            if (int(ending_month) - int(starting_month) + 1) == 6:
                pusg = str((int(ending_month)) / 6)
                data_of_file += "\n    <TaksPusgads>" + pusg + "</TaksPusgads>"

        # getting company VAT number (company registry):
        vat_no = obj_company.partner_id.vat
        if vat_no:
            vat_no = vat_no.replace(' ','').upper()
            vat = vat_no[2:]
            data_of_file += "\n    <NmrKods>" + str(vat) + "</NmrKods>"
        if not vat_no:
            vat = obj_company.company_registry
            data_of_file += "\n    <NmrKods>" + str(vat) + "</NmrKods>"
            if not vat:
                raise osv.except_osv(_('Insufficient data!'), _('No VAT or Company Registry number associated with your company.'))

        # getting e-mail and phone:
        default_address = obj_partner.address_get(cr, uid, [obj_company.partner_id.id])
        default_address_id = default_address.get("default", obj_company.partner_id.id)
        address_id= obj_partner.browse(cr, uid, default_address_id, context)
        if address_id.email:
            data_of_file += "\n    <Epasts>" + address_id.email + "</Epasts>"
        if address_id.phone:
            phone = address_id.phone.replace('.','').replace('/','').replace('(','').replace(')','').replace(' ','')
            data_of_file += "\n    <Talrunis>" + phone + "</Talrunis>"

        # getting given periods and tax codes:
        periods = obj_acc_period.build_ctx_periods(cr, uid, data['period_from'][0], data['period_to'][0])
        tax_code_ids = obj_tax_code.search(cr, uid, [('parent_id','child_of',data_tax.tax_code_id.id), ('company_id','=',obj_company.id)], context=context)

        # summing up all values in all given periods:
        result_period = []
        data_period = {}
        for p in periods:
            ctx = context.copy()
            ctx['period_id'] = p
            tax_info = obj_tax_code.read(cr, uid, tax_code_ids, ['tax_code','code','sum_period'], context=ctx)
            for item in tax_info:
                tax_code = item['tax_code']
                code = item['code']
                sum_period = item['sum_period']
                if data_period.get((code)):
                    sum_period += data_period[(code)]['sum_period']
                    data_period[(code)].clear()
                if not data_period.get((code)):
                    data_period[(code)] = {'tax_code': tax_code,'code': code, 'sum_period': sum_period}
                result_period.append(data_period[(code)])
        result_period_real = []
        for object in result_period:
            if object != {}:
                result_period_real.append(object)

        for item in result_period_real:
            if (item['code'] == '420') and (item['sum_period'] <= -1000.00):
                amount_overpaid = (item['sum_period']) * (-1)
                data_of_file += "\n    <SummaParm>" + str(amount_overpaid) + "</SummaParm>"
                break

        transfer = data['transfer']
        data_of_file += "\n    <ParmaksUzKontu>" + str(int(transfer)) + "</ParmaksUzKontu>"
        if transfer:
            amount_transfer = data['amount_to_transfer']
            bank_account_id = data['bank_account_id']
            bank_account = self.pool.get('res.partner.bank').browse(cr, uid, bank_account_id[0], context=context)
            iban = "".join(bank_account.acc_number.split(" "))
            data_of_file += "\n    <ParmaksUzKontuSumma>" + str(amount_transfer) + "</ParmaksUzKontuSumma>"
            data_of_file += "\n    <IbanNumurs>" + iban + "</IbanNumurs>"

        add_pvn = False
        for item in result_period_real:
            if item['sum_period'] != 0.00:
                add_pvn = True
                break

        if add_pvn == True:
            data_of_file += "\n    <PVN>"

            for item in result_period_real:
                if (item['tax_code'] == '41') and (item['sum_period'] != 0.00):
                    data_of_file += ("\n        <R41>" + str(item['sum_period']) + "</R41>")
                if item['tax_code'] == '41.1' and (item['sum_period'] != 0.00):
                    data_of_file += ("\n        <R411>" + str(item['sum_period']) + "</R411>")
                if item['tax_code'] == '42' and (item['sum_period'] != 0.00):
                    data_of_file += ("\n        <R42>" + str(item['sum_period']) + "</R42>")
                if item['tax_code'] == '43' and (item['sum_period'] != 0.00):
                    data_of_file += ("\n        <R43>" + str(item['sum_period']) + "</R43>")
                if item['tax_code'] == '45' and (item['sum_period'] != 0.00):
                    data_of_file += ("\n        <R45>" + str(item['sum_period']) + "</R45>")
                if item['tax_code'] == '46' and (item['sum_period'] != 0.00):
                    data_of_file += ("\n        <R46>" + str(item['sum_period']) + "</R46>")
                if item['tax_code'] == '47' and (item['sum_period'] != 0.00):
                    data_of_file += ("\n        <R47>" + str(item['sum_period']) + "</R47>")
                if item['tax_code'] == '48' and (item['sum_period'] != 0.00):
                    data_of_file += ("\n        <R48>" + str(item['sum_period']) + "</R48>")
                if item['tax_code'] == '48.1' and (item['sum_period'] != 0.00):
                    data_of_file += ("\n        <R481>" + str(item['sum_period']) + "</R481>")
                if item['tax_code'] == '48.2' and (item['sum_period'] != 0.00):
                    data_of_file += ("\n        <R482>" + str(item['sum_period']) + "</R482>")
                if item['tax_code'] == '49' and (item['sum_period'] != 0.00):
                    data_of_file += ("\n        <R49>" + str(item['sum_period']) + "</R49>")
                if item['tax_code'] == '50' and (item['sum_period'] != 0.00):
                    data_of_file += ("\n        <R50>" + str(item['sum_period']) + "</R50>")
                if item['tax_code'] == '51' and (item['sum_period'] != 0.00):
                    data_of_file += ("\n        <R51>" + str(item['sum_period']) + "</R51>")
                if item['tax_code'] == '52' and (item['sum_period'] != 0.00):
                    data_of_file += ("\n        <R52>" + str(item['sum_period']) + "</R52>")
                if item['tax_code'] == '53' and (item['sum_period'] != 0.00):
                    data_of_file += ("\n        <R53>" + str(item['sum_period']) + "</R53>")
                if item['tax_code'] == '54' and (item['sum_period'] != 0.00):
                    data_of_file += ("\n        <R54>" + str(item['sum_period']) + "</R54>")
                if item['tax_code'] == '55' and (item['sum_period'] != 0.00):
                    data_of_file += ("\n        <R55>" + str(item['sum_period']) + "</R55>")
                if item['tax_code'] == '56' and (item['sum_period'] != 0.00):
                    data_of_file += ("\n        <R56>" + str(item['sum_period']) + "</R56>")
                if item['tax_code'] == '61' and (item['sum_period'] != 0.00):
                    data_of_file += ("\n        <R61>" + str(item['sum_period']) + "</R61>")
                if item['tax_code'] == '62' and (item['sum_period'] != 0.00):
                    data_of_file += ("\n        <R62>" + str(item['sum_period']) + "</R62>")
                if item['tax_code'] == '63' and (item['sum_period'] != 0.00):
                    data_of_file += ("\n        <R63>" + str(item['sum_period']) + "</R63>")
                if item['tax_code'] == '64' and (item['sum_period'] != 0.00):
                    data_of_file += ("\n        <R64>" + str(item['sum_period']) + "</R64>")
                if item['tax_code'] == '65' and (item['sum_period'] != 0.00):
                    data_of_file += ("\n        <R65>" + str(item['sum_period']) + "</R65>")
                if item['tax_code'] == '66' and (item['sum_period'] != 0.00):
                    data_of_file += ("\n        <R66>" + str(item['sum_period']) + "</R66>")
                if item['tax_code'] == '67' and (item['sum_period'] != 0.00):
                    data_of_file += ("\n        <R67>" + str(item['sum_period']) + "</R67>")
                if item['tax_code'] == '57' and (item['sum_period'] != 0.00):
                    data_of_file += ("\n        <R57>" + str(item['sum_period']) + "</R57>")

            data_of_file += "\n    </PVN>"

            # data for attachment PVN1-I:
            data_of_file += "\n    <PVN1I>"

            d_purchase = {}
            d_purchase_exp = []
            r_purchase = []
            purchase_EU_ids = []
            d_sale = {}
            r_sale = []
            sale_EU_ids = []
            # making separate data lists for different journal types and tax codes:
            account_move_ids = account_move_obj.search(cr, uid, [], context=context)
            for account_move in account_move_obj.browse(cr, uid, account_move_ids, context=context):
                if account_move.period_id.id in periods:
                    if (account_move.journal_id.type == 'purchase') or (account_move.journal_id.type == 'purchase_refund') or (account_move.journal_id.type == 'expense'):
                        if (account_move.journal_id.type == 'purchase') or (account_move.journal_id.type == 'purchase_refund'):
                            d_purchase = self._process_line(cr, uid, account_move.line_id, context=context)
                            if d_purchase['tax_code'] != '64':
                                r_purchase.append(d_purchase)
                        if account_move.journal_id.type == 'expense':
                            d_purchase_exp = self._process_expense(cr, uid, account_move.line_id, context=context)
                            for dp in d_purchase_exp:
                                if dp['tax_code'] != '64':
                                    r_purchase.append(dp)
                        for line in account_move.line_id:
                            if line.tax_code_id.tax_code == '64':
                                purchase_EU_ids.append(account_move.id)
                                break

                    if (account_move.journal_id.type == 'sale') or (account_move.journal_id.type == 'sale_refund'):
                        d_sale = self._process_line(cr, uid, account_move.line_id, context=context)
                        if d_sale['tax_code_l'] in ['41', '41.1', '42', '43', '44', '48.2']:
                            r_sale.append(d_sale)
                        for line in account_move.line_id:
                            if line.partner_id.property_account_position and line.partner_id.property_account_position.name == ('ES PVN maksātājs').decode('utf-8'):
                                sale_EU_ids.append(account_move.id)
                                break

            # processing purchase and purchase_refund journal types:
            d_p_s = {}
            r_p_s = []
            if r_purchase != []:
                for p in r_purchase:
                    # getting document types "A" and "N":
                    if p['amount_untaxed'] >= 1000.0:
                        data_of_file += "\n        <R>"
                        data_of_file += ("\n            <DpValsts>" + unicode(p['partner_country']) + "</DpValsts>")
                        deal_type = "A"
                        if p['partner_vat']:
                            data_of_file += ("\n            <DpNumurs>" + str(p['partner_vat']) + "</DpNumurs>")
                            if (p['tax_code'] == '62') and (p['partner_fpos'] == ('LR PVN maksātājs').decode('utf-8')):
                                deal_type = "A"
                        if (not p['partner_vat']) and (p['tax_code'] == '62'):
                            if p['partner_fpos'] == ('LR PVN maksātājs').decode('utf-8'):
                                raise osv.except_osv(_('Insufficient data!'), _('No VAT defined for Partner "%s", but this partner is defined as a VAT payer. Please define the VAT!') % (p['partner_name']))
                            else:
                                deal_type = "N"
                        if p['tax_code'] == '61':
                            deal_type == "I"
                        if p['tax_code'] == '65':
                            deal_type == "K"
                        data_of_file += ("\n            <DpNosaukums>" + unicode(p['partner_name']) + "</DpNosaukums>")
                        data_of_file += ("\n            <DarVeids>" + deal_type + "</DarVeids>")
                        if p['journal_type'] in ['purchase','expense']:
                            data_of_file += ("\n            <VertibaBezPvn>" + str(p['amount_untaxed']) + "</VertibaBezPvn>")
                            data_of_file += ("\n            <PvnVertiba>" + str(p['amount_tax']) + "</PvnVertiba>")
                        if p['journal_type'] == 'purchase_refund':
                            data_of_file += ("\n            <VertibaBezPvn>" + str(p['amount_untaxed'] * (-1)) + "</VertibaBezPvn>")
                            data_of_file += ("\n            <PvnVertiba>" + str(p['amount_tax'] * (-1)) + "</PvnVertiba>")
                        doc_type = "1"
                        if p['invoice_id']:
                            invoice = self.pool.get('account.invoice').browse(cr, uid, p['invoice_id'], context=context)
                            if invoice.payment_ids:
                                if invoice.payment_ids[0].journal_id.type == 'bank':
                                    doc_type = "3"
                                if invoice.payment_ids[0].journal_id.type == 'cash':
                                    doc_type = "2"
                        if (not p['invoice_id']) and (p['journal_type'] != 'expense'):
                            doc_type = "5"
                        data_of_file += ("\n            <DokVeids>" + doc_type + "</DokVeids>")
                        data_of_file += ("\n            <DokNumurs>" + unicode(p['doc_number']) + "</DokNumurs>")
                        data_of_file += ("\n            <DokDatums>" + str(p['doc_date']) + "</DokDatums>")
                        data_of_file += ("\n        </R>")

                    # summing up, what's left for each partner:
                    if (p['amount_untaxed'] < 1000.0) and p['partner_id']:
                        partner_id = p['partner_id']
                        partner_country = p['partner_country']
                        partner_vat = p['partner_vat']
                        partner_name = p['partner_name']
                        if p['journal_type'] in ['purchase', 'expense']:
                            amount_untaxed = p['amount_untaxed']
                            amount_tax = p['amount_tax']
                            amount_taxed = p['amount_taxed']
                        if p['journal_type'] == 'purchase_refund':
                            amount_untaxed = p['amount_untaxed'] * (-1)
                            amount_tax = p['amount_tax'] * (-1)
                            amount_taxed = p['amount_taxed'] * (-1)
                        if d_p_s.get((partner_id)):
                            amount_untaxed += d_p_s[(partner_id)]['amount_untaxed']
                            amount_tax += d_p_s[(partner_id)]['amount_tax']
                            amount_taxed += d_p_s[(partner_id)]['amount_taxed']
                            d_p_s[(partner_id)].clear()
                        if not d_p_s.get((partner_id)):
                            d_p_s[(partner_id)] = {'partner_id': partner_id, 'partner_country': partner_country, 'partner_vat': partner_vat, 'partner_name': partner_name, 'amount_untaxed': amount_untaxed, 'amount_tax': amount_tax, 'amount_taxed': amount_taxed}
                        r_p_s.append(d_p_s[(partner_id)])

                r_p_s_t = []
                for object in r_p_s:
                    if object != {}:
                        r_p_s_t.append(object)

                d_p_a = {}
                amount_untaxed_a = 0.0
                amount_tax_a = 0.0
                amount_taxed_a = 0.0
                for rpst in r_p_s_t:
                    # getting document type "V":
                    if rpst['amount_untaxed'] >= 1000.0:
                        data_of_file += "\n        <R>"
                        data_of_file += ("\n            <DpValsts>" + unicode(rpst['partner_country']) + "</DpValsts>")
                        if rpst['partner_vat']:
                            data_of_file += ("\n            <DpNumurs>" + str(rpst['partner_vat']) + "</DpNumurs>")
                        data_of_file += ("\n            <DpNosaukums>" + unicode(rpst['partner_name']) + "</DpNosaukums>")
                        data_of_file += ("\n            <DarVeids>" + "V" + "</DarVeids>")
                        data_of_file += ("\n            <VertibaBezPvn>" + str(rpst['amount_untaxed']) + "</VertibaBezPvn>")
                        data_of_file += ("\n            <PvnVertiba>" + str(rpst['amount_tax']) + "</PvnVertiba>")
                        data_of_file += ("\n        </R>")
                    # summing up, what's left:
                    if rpst['amount_untaxed'] < 1000.0:
                        amount_untaxed_a += rpst['amount_untaxed']
                        amount_tax_a += rpst['amount_tax']
                        amount_taxed_a += rpst['amount_taxed']

                # putting in values for document type "T":
                d_p_a = {'amount_untaxed': amount_untaxed_a, 'amount_tax': amount_tax_a, 'amount_taxed': amount_taxed_a}
                if d_p_a['amount_taxed'] != 0.0:
                    data_of_file += "\n        <R>"
                    data_of_file += ("\n            <DarVeids>" + "T" + "</DarVeids>")
                    data_of_file += ("\n            <VertibaBezPvn>" + str(d_p_a['amount_untaxed']) + "</VertibaBezPvn>")
                    data_of_file += ("\n            <PvnVertiba>" + str(d_p_a['amount_tax']) + "</PvnVertiba>")
                    data_of_file += ("\n        </R>")

                data_of_file += "\n    </PVN1I>"

            # getting purchases from EU:
            if purchase_EU_ids != []:
                data_of_file += "\n    <PVN1II>"

                for p_EU in account_move_obj.browse(cr, uid, purchase_EU_ids, context=context):
                    for line in p_EU.line_id:
                        if line.partner_id and line.partner_id.vat:
                            partner_country = line.partner_id.vat[:2]
                            partner_vat = line.partner_id.vat[2:]
                        if line.partner_id and not line.partner_id.vat:
                            raise osv.except_osv(_('Insufficient data!'), _('No VAT or Country defined for Partner "%s", but there have been purchases from outside of your country from this partner. Please define the VAT!') % (line.partner_id.name))
                        partner_name = line.partner_id.name
                        deal_type = "C"
                        if line.product_id and line.product_id.type != 'service':
                            deal_type = "G"
                        if line.product_id and line.product_id.type == 'service':
                            deal_type = "P"
                        if not line.tax_code_id:
                            val_taxed_LVL = line.debit or line.credit
                            val_taxed_cur = line.amount_currency
                            if val_taxed_cur < 0:
                                val_taxed_cur = line.amount_currency * (-1)
                        if line.tax_code_id and self._check_tax_code(cr, uid, line.tax_code_id.id, context=context) and (line.tax_code_id.tax_code == '64'):
                            val_tax_LVL = line.credit or line.debit
                            val_tax_cur = line.amount_currency
                        currency = line.currency_id and line.currency_id.name
                        if line.invoice:
                            doc_number = line.invoice.number
                            doc_date = line.invoice.date_invoice
                        if not line.invoice:
                            doc_number = line.move_id.name
                            doc_date = line.move_id.date

                    val_untaxed_LVL = val_taxed_LVL - val_tax_LVL
                    val_untaxed_cur = val_taxed_cur - val_tax_cur
                
                    data_of_file += "\n        <R>"

                    data_of_file += "\n            <DpValsts>" + unicode(partner_country) + "</DpValsts>"
                    data_of_file += "\n            <DpNumurs>" + str(partner_vat) + "</DpNumurs>"
                    data_of_file += "\n            <DpNosaukums>" + unicode(partner_name) + "</DpNosaukums>"
                    data_of_file += "\n            <DarVeids>" + str(deal_type) + "</DarVeids>"
                    data_of_file += "\n            <VertibaBezPvn>" + str(val_untaxed_LVL) + "</VertibaBezPvn>"
                    data_of_file += "\n            <PvnVertiba>" + str(val_tax_LVL) + "</PvnVertiba>"
                    data_of_file += "\n            <ValVertiba>" + str(val_untaxed_cur) + "</ValVertiba>"
                    data_of_file += "\n            <ValKods>" + str(currency) + "</ValKods>"
                    data_of_file += "\n            <DokNumurs>" + unicode(doc_number) + "</DokNumurs>"
                    data_of_file += "\n            <DokDatums>" + str(doc_date) + "</DokDatums>"

                    data_of_file += "\n        </R>"

                data_of_file += "\n    </PVN1II>"

            # processing sale and sale_refund journal types:
            if r_sale != []:
                data_of_file += "\n    <PVN1III>"

                amount_untaxed_x = 0.0
                amount_tax_x = 0.0
                amount_taxed_x = 0.0
                d_s_s = {}
                r_s_s = []
                for s in r_sale:
                    # getting document types "X" or numbers:
                    if s['amount_untaxed'] >= 1000.0:
                        # number document types:
                        if s['partner_fpos'] == ('LR PVN maksātājs').decode('utf-8'):
                            if not s['partner_vat']:
                                raise osv.except_osv(_('Insufficient data!'), _('No VAT defined for Partner "%s", but this partner is marked as VAT payer. Please define the VAT!') % (s['partner_name']))
                            else:
                                data_of_file += "\n        <R>"
                                data_of_file += ("\n            <DpValsts>" + unicode(s['partner_country']) + "</DpValsts>")
                                data_of_file += ("\n            <DpNumurs>" + str(s['partner_vat']) + "</DpNumurs>")
                                data_of_file += ("\n            <DpNosaukums>" + unicode(s['partner_name']) + "</DpNosaukums>")
                                data_of_file += ("\n            <DarVeids>" + str(s['tax_code_l']) + "</DarVeids>")
                                data_of_file += ("\n            <VertibaBezPvn>" + str(s['amount_untaxed']) + "</VertibaBezPvn>")
                                data_of_file += ("\n            <PvnVertiba>" + str(s['amount_tax']) + "</PvnVertiba>")
                                doc_type = "1"
                                if s['invoice_id']:
                                    invoice = self.pool.get('account.invoice').browse(cr, uid, s['invoice_id'], context=context)
                                    if invoice.payment_ids:
                                        if invoice.payment_ids[0].journal_id.type == 'bank':
                                            doc_type = "3"
                                        if invoice.payment_ids[0].journal_id.type == 'cash':
                                            doc_type = "2"
                                if not s['invoice_id']:
                                    doc_type = "5"
                                data_of_file += ("\n            <DokVeids>" + doc_type + "</DokVeids>")
                                data_of_file += ("\n            <DokNumurs>" + unicode(s['doc_number']) + "</DokNumurs>")
                                data_of_file += ("\n            <DokDatums>" + str(s['doc_date']) + "</DokDatums>")
                                data_of_file += "\n        </R>"
                        # "X" document types:
                        if (s['partner_fpos'] == ('LR PVN nemaksātājs').decode('utf-8')) or (not s['partner_vat']):
                            amount_untaxed_x += s['amount_untaxed']
                            amount_tax_x += s['amount_tax']
                            amount_taxed_x += s['amount_taxed']
                    # summing up values for each partner:
                    if s['amount_untaxed'] < 1000.0:
                        partner_id = s['partner_id']
                        partner_country = s['partner_country']
                        partner_vat = s['partner_vat']
                        partner_name = s['partner_name']
                        partner_fpos = s['partner_fpos']
                        if s['journal_type'] == 'sale':
                            amount_untaxed = s['amount_untaxed']
                            amount_tax = s['amount_tax']
                            amount_taxed = s['amount_taxed']
                        if s['journal_type'] == 'sale_refund':
                            amount_untaxed = s['amount_untaxed'] * (-1)
                            amount_tax = s['amount_tax'] * (-1)
                            amount_taxed = s['amount_taxed'] * (-1)
                        if d_s_s.get((partner_id)):
                            amount_untaxed += d_s_s[(partner_id)]['amount_untaxed']
                            amount_tax += d_s_s[(partner_id)]['amount_tax']
                            amount_taxed += d_s_s[(partner_id)]['amount_taxed']
                            d_s_s[(partner_id)].clear()
                        if not d_s_s.get((partner_id)):
                            d_s_s[(partner_id)] = {'partner_id': partner_id, 'partner_country': partner_country, 'partner_vat': partner_vat, 'partner_name': partner_name, 'partner_fpos': partner_fpos, 'amount_untaxed': amount_untaxed, 'amount_tax': amount_tax, 'amount_taxed': amount_taxed}
                        r_s_s.append(d_s_s[(partner_id)])

                r_s_s_t = []
                for object in r_s_s:
                    if object != {}:
                        r_s_s_t.append(object)

                d_p_a = {}
                amount_untaxed_t = 0.0
                amount_tax_t = 0.0
                amount_taxed_t = 0.0
                for rsst in r_s_s_t:
                    # getting document type "V":
                    if rsst['amount_untaxed'] >= 1000.0:
                        data_of_file += "\n        <R>"
                        data_of_file += ("\n            <DpValsts>" + unicode(rsst['partner_country']) + "</DpValsts>")
                        data_of_file += ("\n            <DpNumurs>" + str(rsst['partner_vat']) + "</DpNumurs>")
                        data_of_file += ("\n            <DpNosaukums>" + unicode(rsst['partner_name']) + "</DpNosaukums>")
                        data_of_file += ("\n            <VertibaBezPvn>" + str(rsst['amount_untaxed']) + "</VertibaBezPvn>")
                        data_of_file += ("\n            <PvnVertiba>" + str(rsst['amount_tax']) + "</PvnVertiba>")
                        data_of_file += ("\n            <DokVeids>" + "V" + "</DokVeids>")
                        data_of_file += ("\n        </R>")
                    # summing up, what's left:
                    if rsst['amount_untaxed'] < 1000.0:
                        amount_untaxed_t += rsst['amount_untaxed']
                        amount_tax_t += rsst['amount_tax']
                        amount_taxed_t += rsst['amount_taxed']

                # putting in values for document type "T":
                d_s_t = {'amount_untaxed': amount_untaxed_t, 'amount_tax': amount_tax_t, 'amount_taxed': amount_taxed_t}
                if d_s_t['amount_taxed'] != 0.0:
                    data_of_file += "\n        <R>"
                    data_of_file += ("\n            <VertibaBezPvn>" + str(d_s_t['amount_untaxed']) + "</VertibaBezPvn>")
                    data_of_file += ("\n            <PvnVertiba>" + str(d_s_t['amount_tax']) + "</PvnVertiba>")
                    data_of_file += ("\n            <DokVeids>" + "T" + "</DokVeids>")
                    data_of_file += ("\n        </R>")

                # putting in values for document type "X":
                d_s_x = {'amount_untaxed': amount_untaxed_x, 'amount_tax': amount_tax_x, 'amount_taxed': amount_taxed_x}
                if d_s_x['amount_taxed'] != 0.0:
                    data_of_file += "\n        <R>"
                    data_of_file += ("\n            <VertibaBezPvn>" + str(d_s_x['amount_untaxed']) + "</VertibaBezPvn>")
                    data_of_file += ("\n            <PvnVertiba>" + str(d_s_x['amount_tax']) + "</PvnVertiba>")
                    data_of_file += ("\n            <DokVeids>" + "X" + "</DokVeids>")
                    data_of_file += ("\n        </R>")

                data_of_file += "\n    </PVN1III>"

            # getting sales from EU:
            if sale_EU_ids != []:
                data_of_file += "\n    <PVN2>"

                for s_EU in account_move_obj.browse(cr, uid, sale_EU_ids, context=context):
                    for line in s_EU.line_id:
                        if line.partner_id and line.partner_id.vat:
                            partner_country = line.partner_id.vat[:2]
                            partner_vat = line.partner_id.vat[2:]
                        if line.partner_id and not line.partner_id.vat:
                            raise osv.except_osv(_('Insufficient data!'), _('No VAT or Country defined for Partner "%s", but there have been sales to outside of your country to this partner. Please define the VAT!') % (line.partner_id.name))
                        partner_name = line.partner_id.name
                        deal_type = "C"
                        if line.product_id and line.product_id.type != 'service':
                            deal_type = "G"
                        if line.product_id and line.product_id.type == 'service':
                            deal_type = "P"
                        if not line.tax_code_id:
                            amount_taxed = line.debit or line.credit
                
                    data_of_file += "\n        <R>"

                    data_of_file += "\n            <Valsts>" + unicode(partner_country) + "</Valsts>"
                    data_of_file += "\n            <PVNNumurs>" + str(partner_vat) + "</PVNNumurs>"
                    data_of_file += "\n            <Summa>" + str(amount_taxed) + "</Summa>"
                    data_of_file += "\n            <Pazime>" + str(deal_type) + "</Pazime>"

                    data_of_file += "\n        </R>"

                data_of_file += "\n    </PVN2>"

        data_of_file += "\n</DokPVNv4>"

        data_of_file_real = base64.encodestring(data_of_file.encode('utf8'))
        self.write(cr, uid, ids, {'file_save': data_of_file_real, 'name': data_tax.name}, context=context)
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'l10n_lv.vat.declaration',
            'view_type': 'form',
            'view_mode': 'form',
            'res_id': data_tax.id,
            'views': [(False,'form')],
            'target': 'new',
        }

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
