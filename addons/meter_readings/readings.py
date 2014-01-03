# -*- coding: utf-8 -*-
from osv import fields, osv

import logging
import time
import datetime

_logger = logging.getLogger(__name__)

class mr_readings(osv.osv):
    _name = 'mr.readings'





    def write(self, cr, uid, ids, vals, context=None):
        _logger.warning("vals %s", vals )

        return super(mr_readings, self).write(cr, uid, ids, vals, context=context)

    def _set_new_reading(self, cr, uid, ids, value_now,arg, context=None):
        res = {}
        for m in self.browse(cr, uid, ids, context=context):
            res['value_diff'] = m.value_now - m.value_last
        return {'value':res}


    _columns = {
        'name': fields.char('Name', size=20),
        'mr_reading_id': fields.many2one('mr.counters', 'Id', select=True),
        'value_last': fields.float('Last Value', digits=(15,2)),
        'value_now': fields.float('Now Value', digits=(15,2)),
        'value_diff': fields.float('Diff Value', digits=(15,2)),
        #'value_diff': fields.function(_set_new_reading, string="Diff Value", type='float', digits=(15,2)),
        'period_value': fields.integer('Period', required=True, help="Period month from 1 to 12."),
        'period_date_start':fields.date('Period Start',help="date value in",  required=True),
        'period_date_end':fields.date('Period End',help="date value in" , required=True),
        'it_correct': fields.boolean('It Correct', help="podtverzdenija pakazanij "),
        'it_nulled': fields.boolean('It Nulled', help="Sbros s4e4ika "),

    }

    #_defaults={
     #   'date_in': fields.date.context_today,
     #   }


    def on_change_period_date_start(self, cr, uid, ids, period_date_start=False, context=None):

        res = {}

        pds = time.strptime(period_date_start, "%Y-%m-%d")
        pyear = pds.tm_year
        pmon = pds.tm_mon
        if pmon<10:
            uni_period = '%d0%d' % (pyear , pmon)
        else:
            uni_period = '%d%d' % (pyear , pmon)

        _logger.warning("year %s", uni_period )

        res['name'] = uni_period
        res['period_value'] = int(uni_period)
        return {'value':res}

    def on_change_value_now(self, cr, uid, ids, value_now, value_last,it_nulled,  context=None):

        res = {}
        if context is None: context = {}

        if it_nulled == False:

            res2 = self.pool.get('mr.readings').search(cr, uid,
                [
                    ('mr_reading_id', '=', context.get('counter_id'))
                ],
                order='period_value desc')


            sub_obj = self.pool.get('mr.readings')


            sub2 = {}
            for sub in sub_obj.browse(cr, uid, res2):
                sub2[sub.period_value] = sub.value_now

            value_last_from = sub2[max(sub2)]

            _logger.warning("sub max  =  %s", value_last_from)
            _logger.warning("subs =  %s", sub2 )

        else:
            value_last_from = value_last

        res['value_last'] = value_last_from
        res['value_diff'] = value_now - value_last_from


        return {'value':res}

mr_readings()




class mr_counters(osv.osv):
    _name = 'mr.counters'
    _inherit = 'mr.counters'
    _columns = {
        'mr_readings_ids': fields.one2many('mr.readings', 'mr_reading_id', 'Meter Readings'),
        }
mr_counters()

