# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools, _
import logging
logger = logging.getLogger(__name__)

##Raza
class BiRaza(models.Model):
    _name = 'bi.raza'
    _inherit = ['mail.thread']
    _description = 'Raza del ave'
    name = fields.Char(string='Name', required=True)

##Proveedor
class BiProveedor(models.Model):
    _name = 'bi.proveedor'
    _inherit = ['mail.thread']
    _description = 'Proveedores'

    name = fields.Char(string='Nombre', required=True)

#Solicitud del ave
class BiParvada(models.Model):
    _name = 'bi.parvada'
    _inherit = ['mail.thread']
    _description = 'Parvadas'

    def _get_proveedor(self):
        return self.env['bi.proveedor'].search([],limit=1)
    def _get_raza(self):
        return self.env['bi.raza'].search([], limit=1)

    seq = fields.Char(readonly=True)
    name = fields.Char(string='Numero de parvada',required=True)
    fecha_solicitud = fields.Date(default=fields.Date.context_today, required=True,
                                  help="Fecha en la que se solicito el ave")
    fecha_nacimiento = fields.Date(default=fields.Date.context_today, required=True,
                                  help="Fecha requerida para generar calculos de KPIs")

    proveedor_id = fields.Many2one(comodel_name='bi.proveedor', string="Proveedor", default=_get_proveedor,help="Granja del proveedor de donde proviene el ave")

    poblacion_solicitada = fields.Integer(string='Poblacion Solicitada', required=True, help="Poblacion solicitada")
    edad_sem_tot = fields.Integer(string='Edad Ave (Semanas)', default=0, required=True, help="Edad del ave solicitada")
    poblacion_recepcionada = fields.Integer(string='Poblacion Recepcionada', compute='_compute_poblacion_recepcionada',help="La poblacion recepcionada, sucede cuando se hace una recepcion")
    poblacion_final = fields.Integer(string="Poblacion Final",compute='_compute_poblacion_recepcionada',help="Poblacion final de la solicitud")
    raza_id = fields.Many2one(
        comodel_name='bi.raza', string="Raza", default=_get_raza, required=True)
    state = fields.Selection([('draft', 'Borrador'),
                              ('requested', 'Solicitado'),
                              ('partially_received','Recibido Parcial'),
                              ('received','Recibido'),
                              ('cancel','Cancelado')], default='draft', string="Estado")
    # para postura
    state_postura = fields.Selection([('draft', 'Borrador'),
                              ('transit', 'En Transito'),
                              ('partially_received', 'Recibido Parcial'),
                              ('received', 'Recibido'),
                              ('cancel', 'Cancelado')], default='draft', string="Estado")

    #validacion del numero de parvada
    _sql_constraints = [
        ('name_uniq', 'UNIQUE(name)', 'El numero de parvada ya existe')
    ]

    @api.multi
    @api.depends('poblacion_final')
    def _compute_poblacion_recepcionada(self):
        for r in self:
            suma_recepciones_by_solicitud = 0
            recepciones_objs = self.env['bi.parvada.recepcion'].search([('parvada_id', '=', r.id)])
            for rec in recepciones_objs:
                if rec.state != 'cancel':
                    suma_recepciones_by_solicitud += rec.poblacion_entrante

            r.poblacion_recepcionada = suma_recepciones_by_solicitud
            r.poblacion_final = r.poblacion_solicitada - r.poblacion_recepcionada

            if r.poblacion_final ==0:
                r.write({'state': 'received'})
            else:
                r.write({'state': 'partially_received'})

            if r.poblacion_final == r.poblacion_solicitada:
                r.write({'state': 'requested'})

    #Acciones de Status
    @api.one
    def cancel_progressbar(self):
            self.write({
                'state': 'cancel'
            })

    @api.one
    def request_progressbar(self):
        self.write({
            'state': 'requested'
        })

    @api.one
    def transit_progressbar(self):
        self.write({
            'state_postura': 'transit'
        })

    @api.model
    def create(self, vals):
        seq = self.env['ir.sequence'].next_by_code('bi.parvada') or '/'
        vals['seq'] = seq
        return super(BiParvada, self).create(vals)
