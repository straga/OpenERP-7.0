# -*- coding: utf-8 -*-
from osv import fields, osv


class mr_virtual_counters(osv.osv):
    _name = "mr.virtual.counters"
    _description = "Virtual Counters"
    _columns = {
        'sequence': fields.integer('Counters Sequence ', required=True),
       # 'virtual_counter_id': fields.many2one('mr.counters', 'Id', required=True, ondelete='cascade'),
        'virtual_counter_id': fields.integer('Id'),
        'parent_counter_id': fields.many2one('mr.counters', 'Parent', change_default=True, select=True),
        'description': fields.char('Decriptions'),
        'operation_type': fields.selection([
            ('start','Start'),
            ('plus','Plus'),
            ('minus','Minus'),
            ('end','End'),
            ],'Operation Type', select=True, change_default=True),

    }
mr_virtual_counters()


class mr_counters(osv.osv):
    _name = 'mr.counters'
    _inherit = 'mr.counters'
    _columns = {
        'virtual_counter_ids': fields.one2many('mr.virtual.counters', 'virtual_counter_id', 'Virtual Counter'),
        }
mr_counters()
