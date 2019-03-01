# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import fields, models, api

#REGISTRO BOLETA DE SALIDA
class BiRegistroBoletaSalida(models.Model):
    _name = 'bi.registro.boleta.salida'
    _description = 'Registro de boleta de salida'

    def _get_granja(self):
        return self.env['bi.granja'].search([], limit=1)

    granja_id = fields.Many2one(comodel_name='bi.granja',string="Granja",
                        default=_get_granja, required=True)

    caja_chico = fields.Integer(string="Caja Chico")
    caja_360 = fields.Integer(string="Caja 360")
    sobra_pz_360 = fields.Integer(string="Sobra Pieza 360")
    caja_jumbo = fields.Integer(string="Caja Jumbo")
    caja_180 = fields.Integer(string="Caja 180")
    caja_sucio = fields.Integer(string="Caja Sucio")
    caja_cascado = fields.Integer(string="Caja Cascado")
    caja_deforme = fields.Integer(string="Caja Deforme")
    caja_roto = fields.Integer(string="Caja Roto")
    bolsa_desyemado = fields.Integer(string="Bolsa Desyemado")
    caja_12_nero = fields.Integer(string="Caja 12 Nero")
    caja_18_nero = fields.Integer(string="Caja 18 Nero")
    fecha_registro = fields.Date(default=fields.Date.context_today)
    state = fields.Boolean(string="Estado")



