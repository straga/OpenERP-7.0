##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2013 Prolv (<http://prolv.net>).
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
{
    "name" : "Aimax PressForm",
    "version" : "1.0",
    "author" : "Viktor Vorobjov",
    "category" : "Generic Modules",
    "depends" : ["product"],
    "init_xml" : [],
    "demo_xml" : [],
    "description": "A module that add PressForm atribute for manufactured product ...",
    "update_xml" : [
        "aimax_pressform_view.xml",
        "aimax_pressform_options_view.xml",
        "aimax_pressform_productsize_view.xml",
        "security/ir.model.access.csv",
        ],
    "active": False,
    "installable": True,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
