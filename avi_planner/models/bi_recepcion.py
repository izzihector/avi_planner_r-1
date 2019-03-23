# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError, ValidationError
import logging
logger = logging.getLogger(__name__)

# RECEPCION
class BiParvadaRecepcion(models.Model):
    _name = 'bi.parvada.recepcion'
    _inherit = ['mail.thread']
    _description = 'Recepcion de Aves'

    def _get_solicitud(self):
        return self.env['bi.parvada'].search([('state','=','transit'),('state','=','partially_received')], limit=1)

    name = fields.Char('Lote', readonly=True)
    fecha_recepcion = fields.Date(default=fields.Date.context_today, required=True, string="Fecha de Recepcion")
    fecha_nacimiento = fields.Date(default=fields.Date.context_today, required=True,
                                   help="Fecha requerida para generar calculos de KPIs")
    parvada_id = fields.Many2one(comodel_name='bi.parvada', string="Parvada", default=_get_solicitud, required=True)
    poblacion_entrante = fields.Integer(string="Aves Entrantes", required=True,help="En el formato de Crianza el campo se llama Recepcion")
    folio = fields.Char(string="Folio")
    #estos campos no son almacenados en la tabla
    s_poblacion_solicitada = fields.Integer(related='parvada_id.poblacion_solicitada',string="Poblacion Solicitada")
    s_poblacion_recepcionada = fields.Integer(related='parvada_id.poblacion_recepcionada',string="Poblacion Recepcionada")
    s_poblacion_sin_recepcion = fields.Integer(related='parvada_id.poblacion_final', string="Poblacion Sin Recepcionar")
    s_edad_ave = fields.Integer(related='parvada_id.edad_sem_tot',string="Edad del Ave")
    caseta_id = fields.Many2one(comodel_name='bi.granja.caseta', string="Caseta")
    granja_id = fields.Many2one(comodel_name='bi.granja', string="Granja")
    tipo_granja = fields.Char(related='granja_id.tipo_granja_id.name', string="Tipo de Granja")
    es_postura = fields.Boolean()
    state = fields.Selection([('draft','Borrador'),
                              ('received','Recepcionado'),
                              ('cancel','Cancelado')],default='draft',string="Estado")

    #Secuencia de recepcion
    @api.model
    def create(self, vals):
        seq = self.env['ir.sequence'].next_by_code('bi.parvada.recepcion') or '/'
        vals['name'] = seq
        return super(BiParvadaRecepcion, self).create(vals)

    #Acciones de Status
    @api.one
    def cancel_progressbar(self):
        self.write({
            'state': 'cancel'
        })

####################################################### working on it
    @api.one
    def received_progressbar(self):
        #crea la relacion entre la granja y la parvada
        parvada_granja_obj = self.env['bi.granja.caseta'].search([('granja_id','=',self.granja_id.id),('id','=',self.caseta_id.id)])

        if parvada_granja_obj.parvada_id.id is False:
            parvada_granja_obj.write({'parvada_id': self.parvada_id.id})
        ##crear relacion
        #obj = {
        #     'name': self.parvada_id.name,
        #     'parvada_id': self.parvada_id.id,
        #     'granja_seccion_caseta_id': self.granja_seccion_caseta_destino_rel_id.id
        #}
        #if parvada_granja_rel.id is False:
        #    parvada_granja_obj.create(obj)

        self.write({
            'state': 'received'
        })

    @api.onchange('poblacion_entrante')
    def _onchange_spoblacion_recepcionada(self):
        self.s_poblacion_recepcionada += self.poblacion_entrante
        self.s_poblacion_sin_recepcion -= self.poblacion_entrante

    # revision de la cantidad a recepcionar
    @api.multi
    @api.constrains('poblacion_entrante')
    def checkQuantities(self):
        for r in self:
            if r.poblacion_entrante <= 0:
                raise ValidationError(_('La recepcion debe ser mayor a ZERO'))

            #Revisar que la recepcion no sea mayor a la capacidad maxima de todas las casetas de la granja
            if r.state == 'progress':
                granja_caseta_destino_objs = self.env['bi.granja.caseta'].search([('granja_id','=',r.granja_id.id)])
                sum_capacidad_maxima = 0
                sum_poblacion_final = 0

                for m in granja_caseta_destino_objs:
                    sum_capacidad_maxima += m.capacidad_maxima
                    sum_poblacion_final += m.poblacion_existente

                lugares_disponibles = sum_capacidad_maxima - sum_poblacion_final
                if lugares_disponibles < 0:
                    raise ValidationError(_('La recepcion sobrepasa la capacidad maxima de la granja'))

            if r.s_poblacion_recepcionada > r.s_poblacion_solicitada:
                raise ValidationError(_('La recepcion sobrepasa la poblacion solicitada'))