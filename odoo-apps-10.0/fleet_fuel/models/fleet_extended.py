# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.

from datetime import date, datetime
from odoo import models, fields, api, _
from odoo.exceptions import Warning, ValidationError
from odoo import tools
from odoo.tools import misc

import logging
_logger = logging.getLogger(__name__)


class fleet_fuel(models.Model):
    _inherit = 'fleet.vehicle'

    limit_fuel = fields.Float(string="Limite Combustible (LTS)")
    period = fields.Selection([('week','Semana')],
                              default='week',string="Periodo")


class vehicle_fuel_log(models.Model):
    _inherit = 'fleet.vehicle.log.fuel'
    _order = 'id desc'

    num_vale = fields.Integer(string="No. de vale")
    year = fields.Integer(string="Año")
    week_year = fields.Integer(string="Semana del año")
    state = fields.Selection([('draft', 'Borrador'),
                              ('transit', 'En Transito'),
                              ('loaded', 'Cargado'),
                              ('cancel', 'Cancelado')], default='draft', string="Estado")

    @api.constrains('liter')
    def check_liters(self):
        my_date = self.date
        num_week_year = datetime.strptime(my_date, '%Y-%m-%d')
        self.year = int(num_week_year.strftime("%Y"))

        limit_liters = self.env['fleet.vehicle'].search([('id', '=', self.vehicle_id.id)])
        logs = self.env['fleet.vehicle.log.fuel'].search([('vehicle_id', '=', self.vehicle_id.id),('year','=',self.year),('week_year','=',int(num_week_year.strftime("%U")))])
        sum_liters = 0
        for l in logs:
            if l.state == 'transit' or l.state == 'loaded':
                sum_liters += l.liter
        if sum_liters > limit_liters.limit_fuel:
            raise ValidationError(_('La cantidad de litros asignados es mayor al limite establecido'))

    @api.model
    def create(self, vals):
        my_date = vals['date']
        num_week_year=datetime.strptime(my_date, '%Y-%m-%d')
        vals['year'] = int(num_week_year.strftime("%Y"))
        vals['week_year'] = int(num_week_year.strftime("%U"))
        vals['state'] = 'transit'
        return super(vehicle_fuel_log, self).create(vals)


        # secuencia de traspasos

    # Acciones de Status
    @api.one
    def cancel_progressbar(self):
        self.write({
            'state': 'cancel'
        })

    @api.one
    def transit_progressbar(self):
        self.write({
            'state': 'transit',
        })

    @api.one
    def loaded_progressbar(self):
        self.write({
            'state': 'loaded',
        })