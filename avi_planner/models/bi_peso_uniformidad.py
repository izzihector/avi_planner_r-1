# -*- coding: utf-8 -*-
#*******************************************************
# @author: Ivan Porras
#*******************************************************

from odoo import fields, models, api

class BiPesoUniformidad(models.Model):
    _name = 'bi.peso.uniformidad'
    _inherit = ['mail.thread']
    _description = 'Peso y Uniformidad de recepciones'


    def _get_granja(self):
        return self.env['bi.granja'].search([], limit=1)

    name = fields.Char('Nombre', readonly=True)
    granja_id = fields.Many2one(comodel_name='bi.granja', string="Granja")
    caseta_id = fields.Many2one(comodel_name='bi.granja.caseta', string="Caseta")
    parvada_id = fields.Many2one(related='caseta_id.parvada_id', string="Parvada", store=True, required=True)
    tipo_granja = fields.Char(related='granja_id.tipo_granja_id.name', readonly=True, string="Tipo Granja")
    lote = fields.Many2one(comodel_name='bi.parvada.recepcion', string="Lote")
    peso = fields.Float(string="Peso Ave")
    peso_huevo = fields.Float(string="Peso Huevo")
    uniformidad = fields.Float(string="Uniformidad")
    fecha = fields.Date(default=fields.Date.context_today, required=True,
                                  help="Fecha")

    @api.model
    def create(self, vals):
        seq = self.env['ir.sequence'].next_by_code('bi.peso.uniformidad') or '/'
        vals['name'] = seq
        return super(BiPesoUniformidad, self).create(vals)





   



