# -*- coding: utf-8 -*-
#
from odoo import fields, models, api, _
from odoo.exceptions import UserError, ValidationError

#ALIMENTO
class BiAlimento(models.Model):
    _name = 'bi.alimento'
    _inherit = ['mail.thread']
    _description = 'Alimento'

    name = fields.Char(string='Nombre')

#Tipo de evento de alimento (Entrada, Consumo)
class BiTipoEvento(models.Model):
    _name="bi.alimento.tipo.evento"
    _inherit = ['mail.thread']
    _description = 'Tipo de evento de alimento'

    name=fields.Char(string="Evento")

#REGISTRO DE ALIMENTO
class BiRegistroAlimento(models.Model):
    _name = 'bi.registro.alimento'
    _inherit = ['mail.thread']
    _description = 'Registro de alimento'

    name = fields.Char(string="Referencia",readonly="1")

    def _get_granja(self):
        return self.env['bi.granja'].search([], limit=1)
    def _get_alimento(self):
        return self.env['bi.alimento'].search([], limit=1)
    def _get_tipo_evento(self):
        return self.env['bi.alimento.tipo.evento'].search([], limit=1)

    fecha= fields.Date(default=fields.Date.context_today,string="Fecha")
    caseta_id = fields.Many2one(comodel_name='bi.granja.caseta', string="Caseta")
    granja_id = fields.Many2one(comodel_name='bi.granja', default=_get_granja, string="Granja")
    tipo_granja = fields.Char(related='granja_id.tipo_granja_id.name', readonly=True, string="Tipo Granja")
    parvada_id = fields.Many2one(related='caseta_id.parvada_id', string="Parvada", store=True)
    tipo_evento_id = fields.Many2one(comodel_name='bi.alimento.tipo.evento', string="Tipo de Evento", required=True, default=_get_tipo_evento)
    tolva_id =fields.Many2one(comodel_name='bi.tolva', string="Tolva", required=True, default=None)
    capacidad_tolva = fields.Float(related='tolva_id.capacidad',string="Capacidad de tolva")
    ticket_entrante = fields.Char(string="# Ticket Entrada")
    fleje = fields.Char(string="Fleje")
    alimento_id = fields.Many2one(comodel_name='bi.alimento', string="Fase de Alimento", default=_get_alimento,required=True)
    kgs_entrada = fields.Integer(string="KGS. Entrada")

    consumo = fields.Float(string="KGS. Consumo", help="Este campo es capturado por el usuario")

    #para el traspaso
    kgs_traspaso = fields.Integer(string="KGS. Traspaso")
    caseta_destino_id = fields.Many2one(comodel_name='bi.granja.caseta', string="Caseta Destino")
    granja_destino_id = fields.Many2one(related='caseta_destino_id.granja_id', default=_get_granja, string="Granja Destino")
    tolva_destino_id = fields.Many2one(comodel_name='bi.tolva', string="Tolva Destino", default=None)
    capacidad_tolva_destino = fields.Float(related='tolva_destino_id.capacidad',string="Capacidad Tolva Destino")



    state = fields.Selection([('draft','Borrador'),
                              ('finished','Hecho'),
                              ('cancel','Cancelado')],default='draft',string="Estado")

    @api.onchange('granja_id')
    def _onchange_granja(self):
        self.tolva_id = None
        self.tolva_id = self.env['bi.tolva'].search([('granja_seccion_caseta_id','=',self.granja_id.id)])


    @api.onchange('granja_destino_id')
    def _onchange_granja(self):
        if self.tipo_evento_id==3:
            self.tolva_destino_id = None
            self.tolva_destino_id = self.env['bi.tolva'].search([('granja_seccion_caseta_id','=',self.granja_destino_id.id)])

#    @api.constrains('kgs_entrada')
#    def revisa_capacidad_tolva(self):
        #valida que la suma entrante + la cantidad existente NO supere la capacidad de la tolva
#        kgs_totales = self.kgs_entrada + self.kgs_alimento_existente
#        print ('kilos totales: %s',kgs_totales)
#        if kgs_totales > self.capacidad_tolva:
#            raise ValidationError(_('La entrada + la cantidad existente superan la capacidad de la tolva'))


    #validacion del consumo
    #@api.constrains('consumo')
    #def revisa_existencias(self):
    #    if self.kgs_alimento_existente < self.consumo:
    #        raise ValidationError(_('El consumo es MAYOR que las existencias'))


    # secuencia de alimento
    @api.model
    def create(self, vals):
        seq = self.env['ir.sequence'].next_by_code('bi.registro.alimento') or '/'
        vals['name'] = seq
        return super(BiRegistroAlimento, self).create(vals)

        # Acciones de Status

    @api.one
    def cancel_progressbar(self):
        self.write({
            'state': 'cancel'
        })

    @api.one
    def transit_progressbar(self):
        self.write({
            'state': 'finished',
        })





