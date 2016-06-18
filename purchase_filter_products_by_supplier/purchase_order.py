# -*- coding: utf-8 -*-
#
#    Jamotion GmbH, Your Odoo implementation partner
#    Copyright (C) 2013-2015 Jamotion GmbH.
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
#    Created by renzo.meister on 06.06.2016.
#
# imports of python lib
import logging

# imports of openerp
from openerp import models, fields, api, _

# imports from odoo modules

# global variable definitions
_logger = logging.getLogger(__name__)


class PurchaseOrderLine(models.Model):
    # Private attributes
    _inherit = 'purchase.order.line'

    # Default methods

    # Fields declaration

    # compute and search fields, in the same order that fields declaration

    # Constraints and onchanges

    # CRUD methods

    # Action methods
    @api.multi
    def onchange_product_id(self, pricelist_id, product_id, qty, uom_id, partner_id, date_order=False, fiscal_position_id=False, date_planned=False,
                            name=False, price_unit=False, state='draft'):
        result = super(PurchaseOrderLine, self).onchange_product_id(pricelist_id, product_id, qty, uom_id, partner_id, date_order, fiscal_position_id,
                                                                    date_planned, name, price_unit, state)
        #print "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
        #print "partner_id: ", partner_id
        partner = self.env['res.partner'].search([('id', '=', partner_id)])
        #print "partner: ",partner
        pa_id=0
        for record in partner:
            pa_id = record.parent_id.id
            #print "pa_id", pa_id        
            
        supplier_infos = self.env['product.supplierinfo'].search(['|',('name', '=', partner_id),('name','=',pa_id)])
        #print "supplier_infos: ", supplier_infos
        
        product_ids = self.env['product.product']
        for supplier_info in supplier_infos:
             product_ids += supplier_info.product_tmpl_id.product_variant_ids

        result.update({'domain': {'product_id': [('id', 'in', product_ids.ids)]}})

        return result

# Business methods
