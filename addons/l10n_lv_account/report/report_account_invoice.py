import time
from report import report_sxw
from osv import osv

class custom_parser(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(custom_parser, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'time': time,
            'cr':cr,
            'uid': uid,
        })
        
report_sxw.report_sxw('report.l10n_lv_account.invoice',
                       'account.invoice', 
                       'addons/l10n_lv_account/report/report_account_invoice.html',
                       parser=custom_parser)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
