# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError, ValidationError
import logging
logger = logging.getLogger(__name__)

# TRASPASOS
class BiParvadaDistribucion(models.Model):
    _name = 'bi.parvada.distribucion'
    _inherit = ['mail.thread']
    _description = 'Distribucion de Aves'

    def _get_granja(self):
        return self.env['bi.granja'].search([], limit=1)
    def _get_causa_traspaso(self):
        return self.env['bi.causa.traspaso'].search([], limit=1)
    def _get_granja_destino(self):
        return self.env['bi.granja'].search([('tipo_granja_id','=',2)], limit=1)

    name = fields.Char('Nombre', readonly=True)
    fecha_traspaso = fields.Date(default=fields.Date.context_today, string="Fecha traspaso")
    granja_id = fields.Many2one(comodel_name='bi.granja', string="Granja Origen")
    caseta_id = fields.Many2one(comodel_name='bi.granja.caseta', string="Caseta")
    parvada_id = fields.Many2one(related='caseta_id.parvada_id',  string="Parvada", store=True, required=True)
    t_poblacion_traspaso = fields.Integer(string='Cantidad Traspaso')
    granja_destino_id = fields.Many2one(comodel_name='bi.granja', string="Granja Destino",required=True,default=None)
    caseta_destino_id = fields.Many2one(comodel_name='bi.granja.caseta', string="Caseta")

    causa_traspaso_id = fields.Many2one(comodel_name="bi.causa.traspaso", string="Causa del Traspaso", default=_get_causa_traspaso, required=True)
    state = fields.Selection([('draft','Borrador'),
                              ('transit','En Transito'),
                              ('received','Recepcionado'),
                              ('cancel','Cancelado')],default='draft',string="Estado")

    #para la recepcion en postura
    fecha_recepcion = fields.Date(default=fields.Date.context_today,required=True,string="Fecha de Recepcion")
    reales = fields.Integer(string="Aves Recibidas Reales")
    mortalidad_traspaso = fields.Integer(string="Mortalidad al traspaso")



    @api.multi
    @api.constrains('t_poblacion_traspaso')
    def checkQuantities(self):
        for r in self:
            if r.t_poblacion_traspaso <= 0:
                raise ValidationError(_('El traspaso debe ser mayor a ZERO'))


            #if r.d_poblacion_final < 0:
            #    raise ValidationError(_('El traspaso debe ser MENOR a la existencia de la caseta o granja'))

            #granja_caseta_destino_objs = self.env['bi.granja.seccion.caseta'].search([('id','=',r.granja_seccion_caseta_destino_rel_id.id)])
            #lugares_disponibles_casetas = 0

            #for m in granja_caseta_destino_objs:
            #     lugares_disponibles_casetas = m.capacidad_maxima - m.poblacion_final


            #if lugares_disponibles_casetas < 0:
            #    raise ValidationError(_('El traspaso sobrepasa la capacidad maxima de la caseta'))


    @api.multi
    @api.constrains('reales')
    def checkAvesRecibidas(self):
        for r in self:
            if r.state != 'draft':
                if r.reales <=0:
                    raise ValidationError(_('Las aves recibidas deben ser mayor a ZERO'))

    #@api.onchange('t_poblacion_traspaso')
    #def _onchange_t_poblacion_traspaso(self):
    #    self.d_poblacion_final -= self.t_poblacion_traspaso


    #@api.onchange('causa_traspaso_id')
    #def _onchange_causa_traspaso(self):
    #    self.granja_seccion_caseta_destino_rel_id = None
    #    if self.causa_traspaso_id.id == 3:
    #        self.granja_seccion_caseta_destino_rel_id = self.env['bi.granja.seccion.caseta'].search([('tipo_granja_id','=',2)], limit=1)
    #    else:
    #        self.granja_seccion_caseta_destino_rel_id = self.env['bi.granja.seccion.caseta'].search([('tipo_granja_id','=',1)], limit=1)

    # secuencia de traspasos
    @api.model
    def create(self, vals):
        seq = self.env['ir.sequence'].next_by_code('bi.parvada.distribucion') or '/'
        vals['name'] = seq
        return super(BiParvadaDistribucion, self).create(vals)

    #Acciones de Status
    @api.one
    def cancel_progressbar(self):
        self.write({
            'state':'cancel'
        })
    @api.one
    def transit_progressbar(self):
        self.write({
            'state': 'transit',
        })

    @api.one
    def received_progressbar(self):
        self.checkAvesRecibidas()
        parvada_granja_obj = self.env['bi.granja.caseta'].search(
            [('granja_id', '=', self.granja_destino_id.id), ('id', '=', self.caseta_destino_id.id)])
        if parvada_granja_obj.parvada_id.id is False:
            parvada_granja_obj.write({'parvada_id': self.parvada_id.id})

        self.write({
            'state': 'received',
        })

    # This function is triggered when the user clicks on the button 'Set to started'
    @api.one
    def pending_distribute_progressbar(self):
        self.write({
            'state': 'pending_distribute'
        })

    # This function is triggered when the user clicks on the button 'In progress'
    @api.one
    def distributed_progressbar(self):
        self.write({
            'state': 'distributed'
        })

class BiCausaTraspaso(models.Model):
    _name = 'bi.causa.traspaso'
    _inherit = ['mail.thread']
    _description = 'Causa de traspaso de aves'

    name= fields.Char(string="Causa de traspaso")
