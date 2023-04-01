# -*- coding: utf-8 -*-
##############################################################################
#
#    Jupical Technologies Pvt. Ltd.
#    Copyright (C) 2018-TODAY Jupical Technologies(<http://www.jupical.com>).
#    Author: Jupical Technologies Pvt. Ltd.(<http://www.jupical.com>)
#    you can modify it under the terms of the GNU LESSER
#    GENERAL PUBLIC LICENSE (LGPL v3), Version 3.
#
#    It is forbidden to publish, distribute, sublicense, or sell copies
#    of the Software or modified copies of the Software.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU LESSER GENERAL PUBLIC LICENSE (LGPL v3) for more details.
#
#    You should have received a copy of the GNU LESSER GENERAL PUBLIC LICENSE
#    GENERAL PUBLIC LICENSE (LGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from odoo import models


class ResPartnerExt(models.Model):

    _inherit = 'res.partner'
    _description = 'Partner'

    def clear_duplicates(self):
        duplicate_contacts = []
        user_obj = self.env['res.users']
        cale_obj = self.env['calendar.contacts']
        for partner in self:
            if partner.email and partner.id not in duplicate_contacts:
                duplicates = self.search([('id', '!=', partner.id), ('email', '=', partner.email)])
                for dup in duplicates:
                    user = user_obj.search([('partner_id', '=', dup.id)])
                    calender = cale_obj.search([('partner_id', '=', dup.id)])
                    if not user and not calender:
                        duplicate_contacts.append(dup.id)
        self.browse(duplicate_contacts).unlink()
