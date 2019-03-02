# -*- coding: utf-8 -*-
#*******************************************************
# @author: Ivan Porras
#******************************************************

from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError, ValidationError
import logging
logger = logging.getLogger(__name__)

# MORTALIDAD
class BiMortalidad(models.Model):
    _name = 'bi.parvada.mortalidad'
    _inherit = ['mail.thread']
    _description = 'Mortalidad de Aves'

    name = fields.Char('Nombre', readonly=True)


    granja_id = fields.Many2one(comodel_name='bi.granja', string="Granja")
    caseta_id = fields.Many2one(comodel_name='bi.granja.caseta', string="Caseta")
    parvada_id = fields.Many2one(related='caseta_id.parvada_id',  string="Parvada", store=True)
    tipo_granja = fields.Char(related='granja_id.tipo_granja_id.name', readonly=True, string="Tipo Granja")
    poblacion_existente = fields.Integer(related='caseta_id.poblacion_existente', readonly=True, string="Poblacion Existente")
    
    causa_seleccion = fields.Integer(string="Seleccion") # Causa en Crianza
    causa_natural = fields.Integer(string="Naturales") # Causa en Crianza y Postura
    causa_paralitica = fields.Integer(string="Paraliticas") #Causa en Crianza
    causa_prolapsada = fields.Integer(string="Prolapsadas") #Causa en postura
    causa_sacrificada = fields.Integer(string="Sacrificada") #Causa en Postura y Crianza
    
    total_mortalidad = fields.Integer(string="Total", compute="_compute_total_mortalidad")

    fecha = fields.Date(default=fields.Date.context_today, string="Fecha")
    # apartado peso
    peso_ave = fields.Float(string="Peso Real")
    uniformidad_ave = fields.Float(string="Uniformidad Real")

    state = fields.Selection([('draft','Borrador'),
                              ('finished','Hecho'),
                              ('cancel','Cancelado')],default='draft',string="Estado")


# Revisar aunq es necesario
#    @api.one
#    @api.constrains('causa_seleccion','causa_natural','causa_paralitica','causa_prolapsada','causa_sacrificada')
#    def checkQuantities(self):
#        if self.d_poblacion_final < 0:
#            raise ValidationError(_('El total de la mortalidad no puede ser MAYOR a la POBLACION EXISTENTE'))


    @api.multi
    @api.depends('causa_seleccion','causa_natural','causa_paralitica','causa_sacrificada')
    def _compute_total_mortalidad(self):
        for r in self:
            suma_mortalidad = r.causa_seleccion + r.causa_natural + r.causa_paralitica + r.causa_sacrificada
            r.total_mortalidad = suma_mortalidad

    # secuencia de mortalidad
    @api.model
    def create(self, vals):
        seq = self.env['ir.sequence'].next_by_code('bi.parvada.mortalidad') or '/'
        vals['name'] = seq
        return super(BiMortalidad, self).create(vals)

    #Acciones de Status
    @api.one
    def cancel_progressbar(self):
        self.write({
            'state':'cancel'
        })
    @api.one
    def transit_progressbar(self):
        self.write({
            'state': 'finished',
        })

