# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import fields, models

#EMPAQUE
class BiEmpaqueParametros(models.Model):
    _name = 'bi.empaque.parametros'
    _inherit = ['mail.thread']
    _description = 'Empaque Parametros'

    name = fields.Char(string='Nombre',required=True)
    image = fields.Binary()
    order = fields.Integer(string="Orden")
    cinta = fields.Integer(string="Cinta")
    conos = fields.Integer(string="Conos")
    conosGrandes = fields.Integer(string="Cono Grande")
    divisores = fields.Integer(string="Divisores")
    visible = fields.Boolean(string="Visible")
    state = fields.Boolean(string="Activo")

#Empaque
class BIEmpaque(models.Model):
    _name='bi.empaque'
    _inherit = ['mail.thread']
    _description="Empaque"

    name =fields.Char(string='Nombre',required=True)

#REGISTRO EMPAQUE
class BiRegistroEmpaque(models.Model):
    _name = 'bi.registro.empaque'
    _inherit = ['mail.thread']
    _description = 'Registro de empaque'

    def _get_empaque(self):
        return self.env['bi.empaque'].search([], limit=1)

    fecha= fields.Date(default=fields.Date.context_today)
    granja_id = fields.Many2one(comodel_name='bi.granja', string="Granja")
    empaque_id = fields.Many2one(comodel_name='bi.empaque', string="Empaque", default=_get_empaque, required=True)
    entrada = fields.Integer(string="Entrada")
    merma_fabricacion = fields.Integer(string="Merma Fabricacion")
    merma_operacion = fields.Integer(string="Merma Operacion")

    state = fields.Boolean(string="Estado")


class BITraspasoEmpaque(models.Model):
    _name='bi.traspaso.empaque'
    _inherit = ['mail.thread']
    _description="Traspaso de empaque"

    def _get_granja(self):
        return self.env['bi.granja'].search([], limit=1)

    def _get_empaque(self):
        return self.env['bi.empaque'].search([], limit=1)

    fecha= fields.Date(default=fields.Date.context_today)  
    granja_origen__id = fields.Many2one(
        comodel_name='bi.granja', string="Granja Origen", default=_get_granja, required=True)
    empaque_id = fields.Many2one(comodel_name='bi.empaque', string="Empaque", default=_get_empaque, required=True)
    cantidad_traspaso = fields.Integer(string="Cantidad a traspasar")
    granja_destino__id = fields.Many2one(
        comodel_name='bi.granja', string="Granja Destino", default=_get_granja, required=True)
