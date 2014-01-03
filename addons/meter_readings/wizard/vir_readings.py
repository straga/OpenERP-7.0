# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
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
from openerp.tools.translate import _
import logging

_logger = logging.getLogger(__name__) # Need for message in console.



class VirReadings(osv.osv_memory):

    _name = 'mr.vir_readings'
    _description = 'Add Virtual Reading'


    def add_vir_reading(self, cr, uid, ids, context=None):

        # get context or not
        context = context or {}

        _logger.warning("Context = %s", context)

        # it id counter.
        counter_id = context.get('active_id')




        return True


VirReadings()
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

