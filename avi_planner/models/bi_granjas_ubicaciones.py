# -*- coding: utf-8 -*-
from odoo import fields, models, api


# Tipo de Granja
class BiGranjaTipo(models.Model):
    _name = 'bi.granja.tipo'
    _inherit = ['mail.thread']
    _description = 'tipo de granja'
    name = fields.Char(string='Nombre')


# Granja
class BiGranja(models.Model):
    _name = 'bi.granja'
    _inherit = ['mail.thread']
    _description = 'Granjas de postura'

    def _get_tipo_granja(self):
        return self.env['bi.granja.tipo'].search([], limit=1)

    name = fields.Char(string='Nombre')
    tipo_granja_id = fields.Many2one(comodel_name='bi.granja.tipo', string="Tipo", default=_get_tipo_granja,
                                     required=True)
    # TODO:Generar campos de capacidad instalada, capacidad extra en porcentaje, capacidad extra en unidades y capacidad maxima
    #     esto para saber cual es la capadidad de toda la granja sumando las casetas.


# Seccion
class BiSeccion(models.Model):
    _name = 'bi.granja.seccion'
    _inherit = ['mail.thread']
    _description = 'Seccion de la granja'

    def _get_granja(self):
        return self.env['bi.granja'].search([], limit=1)

    name = fields.Char(string='Seccion')
    granja_id = fields.Many2one(comodel_name='bi.granja', string="Granja", default=_get_granja, required=True)


# Caseta
class Bicaseta(models.Model):
    _name = 'bi.granja.caseta'
    _inherit = ['mail.thread']
    _description = 'Casetas en granjas'

    def _get_granja(self):
        return self.env['bi.granja'].search([], limit=1)

    def _get_seccion(self):
        return self.env['bi.granja.seccion'].search([], limit=1)

    name = fields.Char(string='Caseta', required=True)
    granja_id = fields.Many2one(comodel_name='bi.granja', string="Granja", default=_get_granja, required=True)
    seccion_id = fields.Many2one(comodel_name='bi.granja.seccion', string="Seccion", default=_get_seccion)
    capacidad_instalada = fields.Integer(string="Capacidad instalada")
    capacidad_extra_p = fields.Integer(string="Capacidad extra %")
    capacidad_extra_u = fields.Integer(string="Capacidad extra Unidades")
    capacidad_maxima = fields.Integer(string="Capacidad maxima", compute='_compute_capacidad_maxima')
    parvada_id = fields.Many2one(comodel_name='bi.parvada',string="Parvada Asignada")
    poblacion_existente = fields.Integer(string="Poblacion Existente", compute='_compute_poblacion_existente')
    recepciones_ids = fields.Many2many('bi.parvada.recepcion', string="Lotes Asignados",store=True)


    @api.one
    @api.depends('capacidad_instalada', 'capacidad_extra_p', 'capacidad_extra_u')
    def _compute_capacidad_maxima(self):
        capacidad_maxima = (self.capacidad_instalada * self.capacidad_extra_p) / 100 + self.capacidad_instalada
        capacidad_maxima += self.capacidad_extra_u
        self.capacidad_maxima = capacidad_maxima

    @api.multi
    @api.depends('poblacion_existente')
    def _compute_poblacion_existente(self):
        for r in self:
            # suma de entradas
            entradas_objs = self.env['bi.parvada.recepcion'].search(
                [('caseta_id', '=', r.id),
                 ('parvada_id', '=', r.parvada_id.id)])

            suma_entradas = 0
            if entradas_objs is not None:
                for e in entradas_objs:
                    suma_entradas += e.poblacion_entrante

            # suma de traspasos como destino
            suma_traspasos_positivos = 0
            traspasos_objs = self.env['bi.parvada.distribucion'].search([('caseta_destino_id', '=', r.id)])

            if traspasos_objs is not None:
                for t in traspasos_objs:
                    suma_traspasos_positivos += t.t_poblacion_traspaso

            # suma de traspasos como origen
            suma_traspasos_negativos = 0
            traspasos_n_objs = self.env['bi.parvada.distribucion'].search([('caseta_id', '=', r.id)])
            if traspasos_n_objs is not None:
                for tn in traspasos_n_objs:
                    suma_traspasos_negativos += tn.t_poblacion_traspaso
            # suma de mortalidad
            suma_mortalidad = 0
            mortalidad_objs = self.env['bi.parvada.mortalidad'].search([('caseta_id', '=', r.id), ('parvada_id', '=', r.parvada_id.id)])
            if mortalidad_objs is not None:
                for m in mortalidad_objs:
                    suma_mortalidad += m.total_mortalidad

            r.poblacion_existente = (suma_entradas + suma_traspasos_positivos) - suma_traspasos_negativos - suma_mortalidad
