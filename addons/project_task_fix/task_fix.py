# -*- coding: utf-8 -*-

from openerp.osv import fields, osv



class task(osv.osv):

    _inherit = 'project.task'

    _columns = {
        'date_deadline': fields.datetime('Deadline',select=True), #change to datatime
    }

    _order = "date_deadline, priority, sequence, date_start, name, id" #order date_deadline

task()
