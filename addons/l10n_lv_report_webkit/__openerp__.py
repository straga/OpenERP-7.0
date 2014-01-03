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

{
    "name": "Latvian Localization for Webkit reports",
    "description": """
Webkit Report Latvijas lokalizācija
------------------------------------

Logo sagataves:

* logo - logo bez teksta
* logo_text - logo ar tekstu

Header/Footer sagataves:

* A4 LV Portrait Internal - portreta orientācija bez logo
* A4 LV Landscape Internal - ainavas orientācija bez logo
* A4 LV Invoice - rēķins ar logo ar tekstu
* A4 LV Portrait External - portreta orientācija ar logo bez teksta
                    """,
    "version": "0.1",
    "depends": ["report_webkit"],
    "category": "Reporting",
    "author": "ITS-1",
    "url": "http://www.its1.lv",
    "update_xml": ["data.xml",

                   ],
    "installable": True,
    "auto_install": False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
