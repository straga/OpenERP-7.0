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

import base64
import time
from datetime import datetime

from openerp.osv import fields, osv
from openerp.tools.translate import _
from openerp import tools
import openerp.addons.decimal_precision as dp

from xml.dom.minidom import getDOMImplementation, parseString

import logging

_logger = logging.getLogger(__name__)

class account_fidavista_imported_statements(osv.osv_memory):
    _name = "account.fidavista.imported.statements"
    _columns = {
        'wizard_id': fields.many2one('account.fidavista.import', string="Wizard"),
        'last_statement': fields.char('Last statements for selected accounts', size=64),
        'last_balance_end': fields.float('Ending Balance', digits_compute=dp.get_precision('Account')),
        'wrong_balance': fields.boolean('Wrong Balance')
    }

class account_fidavista_importing_statements(osv.osv_memory):
    _name = "account.fidavista.importing.statements"
    _columns = {
        'wizard_id': fields.many2one('account.fidavista.import', string="Wizard"),
        'current_statement': fields.char('Statements to import', size=64),
        'current_balance_start': fields.float('Starting Balance', digits_compute=dp.get_precision('Account')),
        'wrong_balance': fields.boolean('Wrong Balance')
    }

class account_fidavista_import(osv.osv_memory):
    _name = 'account.fidavista.import'
    _description = 'Import FiDAViSta File'
    _columns = {
        'fidavista_data': fields.binary('FiDAViSta File', required=True),
        'fidavista_fname': fields.char('FiDAViSta Filename', size=128, required=True),
        'note': fields.text('Log'),
        'period_id': fields.many2one('account.period', 'Period', help="Select a Period for the Bank Statement.", required=True),
        'flag': fields.boolean('Continue Anyway', help="If checked, continues without comparing balances."),
        'wrong_balance': fields.boolean('Wrong Balance'),
        'imported_statements' : fields.one2many('account.fidavista.imported.statements', 'wizard_id', 'Imported Statements'),
        'importing_statements' : fields.one2many('account.fidavista.importing.statements', 'wizard_id', 'Statements to Import'),
    }

    _defaults = {
        'fidavista_fname': lambda *a: '',
        'flag': False,
        'wrong_balance': False
    }

    def onchange_fidavista_data(self, cr, uid, ids, fidavista_data, fidavista_fname, context=None, fidavistafile=None, fidavistafilename=None):
        # getting data:
        if context is None:
            context = {}
        try:
            fidavistafile = fidavista_data
            fidavistafilename = fidavista_fname
        except:
            raise osv.except_osv(_('Error'), _('Wizard in incorrect state. Please hit the Cancel button'))
            return False

        # decoding and encoding for string parsing; parseString() method:
        record = unicode(base64.decodestring(fidavistafile), 'iso8859-4', 'strict').encode('iso8859-4','strict')
        dom = parseString(record)

        # getting date values:
        prep_date = dom.getElementsByTagName('PrepDate')[0].toxml().replace('<PrepDate>','').replace('</PrepDate>','')
        start_date = dom.getElementsByTagName('StartDate')[0].toxml().replace('<StartDate>','').replace('</StartDate>','')
        end_date = dom.getElementsByTagName('EndDate')[0].toxml().replace('<EndDate>','').replace('</EndDate>','')

        # getting the accountsets to browse through and giving start values for fields:
        accountsets = dom.getElementsByTagName('AccountSet')
        wrong_balance = False
        test_date = False
        period_id = False
        line_date_list = []
        latest_bank_statement_name = False
        latest_bank_statement_balance_end = False
        result_imported = []
        datas_imported = {}
        result_importing = []
        datas_importing = {}
        for company_account in accountsets:
            # testing, whether the Company's bank account is defined in the system:
            company_acc_no = company_account.getElementsByTagName('AccNo')[0].toxml().replace('<AccNo>','').replace('</AccNo>','')
            company_acc_no_list = list(company_acc_no)
            company_acc_no_list.insert(4,' ')
            company_acc_no_list.insert(9,' ')
            company_acc_no_list.insert(14,' ')
            company_acc_no_list.insert(19,' ')
            company_acc_no_list.insert(24,' ')
            company_acc_no_2 = "".join(company_acc_no_list)
            test_acc_no = self.pool.get('res.partner.bank').search(cr, uid, [('acc_number','=',company_acc_no)])
            if not test_acc_no:
                test_acc_no = self.pool.get('res.partner.bank').search(cr, uid, [('acc_number','=',company_acc_no_2)])

            # getting Statement Reference:
            statement_name = company_acc_no + ' ' + start_date+ ':' + end_date

            # getting and checking balances:
            balance_start = company_account.getElementsByTagName('OpenBal')[0].toxml().replace('<OpenBal>','').replace('</OpenBal>','')
            if test_acc_no:
                bank_statement_ids = self.pool.get('account.bank.statement').search(cr, uid, [('bank_account_id', '=', test_acc_no[0])], order='date', context=context)
                if bank_statement_ids:
                    latest_bank_statement = self.pool.get('account.bank.statement').browse(cr, uid, bank_statement_ids[-1], context=context)
                    latest_bank_statement_name = latest_bank_statement.name
                    latest_bank_statement_balance_end = latest_bank_statement.balance_end_real

                    if latest_bank_statement.balance_end_real != float(balance_start):
                        wrong_balance = True

            # creating values for fields:
            datas_imported = {'last_statement': latest_bank_statement_name, 'last_balance_end': latest_bank_statement_balance_end, 'wrong_balance': wrong_balance}
            result_imported.append(datas_imported)

            datas_importing = {'current_statement': statement_name, 'current_balance_start': float(balance_start), 'wrong_balance': wrong_balance}
            result_importing.append(datas_importing)

            # checking statement lines for period dates:
            statement_lines = company_account.getElementsByTagName('TrxSet')
            for line in statement_lines:
                line_date = line.getElementsByTagName('BookDate')[0].toxml().replace('<BookDate>','').replace('</BookDate>','')
                if line_date:
                    line_date_list.append(line_date)
                    break
        if line_date_list != []:
            test_date = line_date_list[0]
        period = self.pool.get('account.period').search(cr, uid, [('date_start','<=',test_date),('date_stop','>=',test_date)], context=context)
        if period:
            if len(period) > 1:
                period_id = period[1]
            else:
                period_id = period[0]

        return {'value': {'period_id': period_id, 'imported_statements': result_imported, 'importing_statements': result_importing, 'wrong_balance': wrong_balance}}


    def fidavista_parsing(self, cr, uid, ids, context=None, fidavistafile=None, fidavistafilename=None, flag=False):
        if context is None:
            context = {}
        # getting elements from object:
        data = self.browse(cr, uid, ids)[0]
        try:
            fidavistafile = data.fidavista_data
            fidavistafilename = data.fidavista_fname
            period_id = data.period_id
            flag = data.flag
        except:
            raise osv.except_osv(_('Error'), _('Wizard in incorrect state. Please hit the Cancel button'))
            return {}

        # decoding and encoding for string parsing; parseString() method:
        record = unicode(base64.decodestring(fidavistafile), 'iso8859-4', 'strict').encode('iso8859-4','strict')
        dom = parseString(record)

        # getting start values:
        prep_date = dom.getElementsByTagName('PrepDate')[0].toxml().replace('<PrepDate>','').replace('</PrepDate>','')
        start_date = dom.getElementsByTagName('StartDate')[0].toxml().replace('<StartDate>','').replace('</StartDate>','')
        end_date = dom.getElementsByTagName('EndDate')[0].toxml().replace('<EndDate>','').replace('</EndDate>','')

        # going through information about the accounts:
        accountsets = dom.getElementsByTagName('AccountSet')
        for company_account in accountsets:

            # testing, whether the Company's bank account is defined in the system:
            company_acc_no = company_account.getElementsByTagName('AccNo')[0].toxml().replace('<AccNo>','').replace('</AccNo>','')
            company_acc_no_list = list(company_acc_no)
            company_acc_no_list.insert(4,' ')
            company_acc_no_list.insert(9,' ')
            company_acc_no_list.insert(14,' ')
            company_acc_no_list.insert(19,' ')
            company_acc_no_list.insert(24,' ')
            company_acc_no_2 = "".join(company_acc_no_list)
            test_acc_no = self.pool.get('res.partner.bank').search(cr, uid, [('acc_number','=',company_acc_no)])
            if not test_acc_no:
                test_acc_no = self.pool.get('res.partner.bank').search(cr, uid, [('acc_number','=',company_acc_no_2)])
                if not test_acc_no:
                    raise osv.except_osv(_('No bank account defined'), _("There is no bank account with number '%s' defined in the system. Please define such account and try again!") %(company_acc_no))
                    return {}

            # getting Statement Reference and Date:
            statement_name = company_acc_no + ' ' + start_date+ ':' + end_date
            statement_date = end_date

            # testing, wheteher there is a journal available for the import:
            currency = company_account.getElementsByTagName('Ccy')[0].toxml().replace('<Ccy>','').replace('</Ccy>','')
            journal_obj = self.pool.get('account.journal')
            journal = journal_obj.search(cr, uid, [('type','=','bank')], context=context)
            journal_id = False
            if journal:
                for jrn in journal_obj.browse(cr, uid, journal, context=context):
                    cur = jrn.currency.name
                    if not cur:
                        cur = jrn.company_id.currency_id.name
                    if cur == currency:
                        journal_id = jrn.id
                        break
            if not journal or journal_id==False:
                raise osv.except_osv(_('No Journal available'), _("There is no Journal of Type 'Bank and Checks' and Currency '%s' currenlty available in the system. Please define such Journal and try again!") %(currency))
                return {}

            # getting and checking balances:
            balance_start = company_account.getElementsByTagName('OpenBal')[0].toxml().replace('<OpenBal>','').replace('</OpenBal>','')
            balance_end_real = company_account.getElementsByTagName('CloseBal')[0].toxml().replace('<CloseBal>','').replace('</CloseBal>','')
            bank_statement_ids = self.pool.get('account.bank.statement').search(cr, uid, [('bank_account_id', '=', test_acc_no[0])], order='date', context=context)
            if bank_statement_ids:
                if flag == False:
                    latest_bank_statement = self.pool.get('account.bank.statement').browse(cr, uid, bank_statement_ids[-1], context=context)
                    if latest_bank_statement.balance_end_real != float(balance_start):
                        raise osv.except_osv(_('Balances do not match!'), _("The Ending Balance of the last Bank Statement (by date) imported for the Bank Account '%s' is not equal to the Starting Balance of this document. If this is OK with you, check the 'Continue Anyway' box and try to import again.") %(company_acc_no))

            # creating account.bank.statement
            statement = self.pool.get('account.bank.statement').create(cr, uid, {'name': statement_name, 'date': statement_date, 'period_id': period_id.id, 'journal_id': journal_id, 'balance_start': balance_start, 'balance_end_real': balance_end_real, 'bank_account_id': test_acc_no[0]}, context=context)

            # getting elements for account.bank.statement.line and creating the lines:
            statement_lines = company_account.getElementsByTagName('TrxSet')
            count = 0
            for line in statement_lines:

                # testing the dates:
                count += 1
                line_date = line.getElementsByTagName('BookDate')[0].toxml().replace('<BookDate>','').replace('</BookDate>','')
                statement_line_ids = self.pool.get('account.bank.statement.line').search(cr, uid, [('statement_id.bank_account_id', '=', test_acc_no[0])], context=context)
                if statement_line_ids:
                    latest_statement_line = self.pool.get('account.bank.statement.line').browse(cr, uid, statement_line_ids[-1], context=context)
                    if (count == 1) and (latest_statement_line.date > line_date):
                        raise osv.except_osv(_('Incorrect dates'), _("The Date of the last Bank Statment Line posted for this Bank Account should not come after the date of the first transaction described in the FiDAViSta file!"))
                        return {}
                if (line_date < period_id.date_start) or (line_date > period_id.date_stop):
                    raise osv.except_osv(_('Incorrect dates'), _("The Date of a Transaction in FiDAViSta file should be inside the period chosen in the wizard!"))
                    return {}
                # getting OBI:
                pmt_info = line.getElementsByTagName('PmtInfo')
                if pmt_info:
                    line_name = pmt_info[0].toxml().replace('<PmtInfo>','').replace('</PmtInfo>','')
                if not pmt_info:
                    line_name = line.getElementsByTagName('TypeName')[0].toxml().replace('<TypeName>','').replace('</TypeName>','')

                # getting Reference:
                line_ref = line.getElementsByTagName('BankRef')[0].toxml().replace('<BankRef>','').replace('</BankRef>','')

                # getting Amount:
                cord = line.getElementsByTagName('CorD')[0].toxml().replace('<CorD>','').replace('</CorD>','')
                if cord == 'C':
                    line_amount = line.getElementsByTagName('AccAmt')[0].toxml().replace('<AccAmt>','').replace('</AccAmt>','')
                if cord == 'D':
                    line_amount = float(line.getElementsByTagName('AccAmt')[0].toxml().replace('<AccAmt>','').replace('</AccAmt>','')) * (-1)

                # getting Partner info:
                account_id = False
                cPartySet = line.getElementsByTagName('CPartySet')
                if cPartySet:
                    partner_name_tag = cPartySet[0].getElementsByTagName('Name')
                    if partner_name_tag:
                        partner_name = partner_name_tag[0].toxml().replace('<Name>','').replace('</Name>','').replace('<Name/>','').replace("&quot;","'")
                    if not partner_name_tag:
                        partner_name = False
                    partner_reg_id_tag = cPartySet[0].getElementsByTagName('LegalId')
                    if partner_reg_id_tag:
                        partner_reg_id = partner_reg_id_tag[0].toxml().replace('<LegalId>','').replace('</LegalId>','').replace('<LegalId/>','')
                    if not partner_reg_id_tag:
                        partner_reg_id = False
                    partner_bank_account_tag = cPartySet[0].getElementsByTagName('AccNo')
                    if partner_bank_account_tag:
                        partner_bank_account = partner_bank_account_tag[0].toxml().replace('<AccNo>','').replace('</AccNo>','').replace('<AccNo/>','')
                    if not partner_bank_account_tag:
                        partner_bank_account = False

                    # testing, whether it's possible to get partner_id (also type and account) from the system:
                    partner_id = False
                    type = 'general'
                    bank_account_obj = self.pool.get('res.partner.bank')
                    bank_account = bank_account_obj.search(cr, uid, [('acc_number','=',partner_bank_account)])
                    if (not bank_account) and partner_bank_account:
                        partner_bank_account_list = list(partner_bank_account)
                        partner_bank_account_list.insert(4,' ')
                        partner_bank_account_list.insert(9,' ')
                        partner_bank_account_list.insert(14,' ')
                        partner_bank_account_list.insert(19,' ')
                        partner_bank_account_list.insert(24,' ')
                        partner_bank_account_2 = "".join(partner_bank_account_list)
                        bank_account = bank_account_obj.search(cr, uid, [('acc_number','=',partner_bank_account_2)])
                    if bank_account:
                        bank_acc_1 = bank_account_obj.browse(cr, uid, bank_account[0])
                        partner_id = bank_acc_1.partner_id.id
                        if bank_acc_1.partner_id.customer and not bank_acc_1.partner_id.supplier:
                            type = 'customer'
                        if bank_acc_1.partner_id.supplier and not bank_acc_1.partner_id.customer:
                            type = 'supplier'
                        if cord == 'C':
                            account_id = bank_acc_1.partner_id.property_account_receivable.id
                        if cord == 'D':
                            account_id = bank_acc_1.partner_id.property_account_payable.id
                    if (not bank_account) and (partner_reg_id):
                        partner_obj = self.pool.get('res.partner')
                        partner_ids = partner_obj.search(cr, uid, [], context=context)
                        for partner in partner_obj.browse(cr, uid, partner_ids, context=context):
                            vat = partner.vat
                            if vat:
                                if vat.find(partner_reg_id) != -1:
                                    partner_id = partner.id
                                    if partner.customer and not partner.supplier:
                                        type = 'customer'
                                    if partner.supplier and not partner.customer:
                                        type = 'supplier'
                                    if cord == 'C':
                                        account_id = partner.property_account_receivable.id
                                    if cord == 'D':
                                        account_id = partner.property_account_payable.id
                                    break

                # values, if there is no <CPartySet> in the document:
                if not cPartySet:
                    partner_name = False
                    partner_reg_id = False
                    partner_bank_account = False
                    partner_id = False
                    type = 'general'

                # getting Transaction Types
                type_code_tag = line.getElementsByTagName('TypeCode')
                type_code = False
                if type_code_tag:
                    type_code = type_code_tag[0].toxml().replace('<TypeCode>','').replace('</TypeCode>','')
                if not type_code_tag:
                    type_name_tag = line.getElementsByTagName('TypeName')
                    if type_name_tag:
                        type_code = type_name_tag[0].toxml().replace('<TypeName>','').replace('</TypeName>','')
                    if not type_name_tag:
                        raise osv.except_osv(_('Tag Error'), _('There are no tags for Transaction Types!'))
                        return {}

                # getting configuration types for Accounts, it there is no Partner:
                if partner_id == False:
                    config_obj = self.pool.get('account.fidavista.transaction.type')
                    config_ids = config_obj.search(cr, uid, [], context=context)
                    for config in config_obj.browse(cr, uid, config_ids, context=context):
                        types_list = config.type.split(", ")
                        for item in types_list:
                            if item == type_code:
                                account_id = config.account_id.id

                if account_id == False:
                    raise osv.except_osv(_('Configuration Error'), _("There is no Partner found in the system, that has a Bank Account or Registration Number as in the FiDAViSta file (if there are any); there is also no Configuration found for the Transaction Type '%s'. Please create either a Partner or a Transaction Type Configuration!") %(type_code))
                    return {}

                # creating account.bank.statement.line:
                self.pool.get('account.bank.statement.line').create(cr, uid, {'statement_id': statement, 'name': line_name, 'date': line_date, 'ref': line_ref, 'partner_name': partner_name, 'partner_reg_id': partner_reg_id, 'partner_bank_account': partner_bank_account, 'transaction_type': type_code, 'partner_id': partner_id, 'type': type, 'account_id': account_id, 'amount': line_amount}, context=context)

        # getting a Bank Statement view to return
        model, action_id = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'account', 'action_bank_statement_tree')
        action = self.pool.get(model).browse(cr, uid, action_id, context=context)
        return {
            'name': action.name,
            'view_type': action.view_type,
            'view_mode': action.view_mode,
            'res_model': action.res_model,
            'domain': action.domain,
            'context': action.context,
            'type': 'ir.actions.act_window',
            'search_view_id': action.search_view_id.id,
            'views': [(v.view_id.id, v.view_mode) for v in action.view_ids]
        }

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
