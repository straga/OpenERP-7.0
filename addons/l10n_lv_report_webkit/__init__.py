# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright (c) 2012 ITS-1 SIA (http://www.its1.lv) 
# All Right Reserved
#
# Author : Jānis Bojārs (its-1)
#
# WARNING: This program as such is intended to be used by professional
# programmers who take the whole responsability of assessing all potential
# consequences resulting from its eventual inadequacies and bugs
# End users who are looking for a ready-to-use solution with commercial
# garantees and support are strongly adviced to contract a Free Software
# Service Company
#
# This program is Free Software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
##############################################################################

import verbose_nums

import verbose_nums
from report_webkit import report_helper
from types import MethodType


# we decorate WebKitHelper to allow num translation to string for Latvian language
def verbose_num_lv(self, num, currency):
    return verbose_nums.convert_currency(num, currency)

report_helper.WebKitHelper.verbose_num_lv = MethodType(verbose_num_lv, None, report_helper.WebKitHelper)


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
