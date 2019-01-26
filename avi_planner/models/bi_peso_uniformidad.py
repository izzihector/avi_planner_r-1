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
    caseta_id = fields.Many2one(comodel_name='bi.granja.caseta', string="Caseta")
    granja_id = fields.Many2one(related='caseta_id.granja_id', default=_get_granja, string="Granja",store=True)
    lote = fields.Many2one(comodel_name='bi.parvada.recepcion', string="Lote")
    peso = fields.Float(string="Peso")
    uniformidad = fields.Float(string="Uniformidad")
    fecha = fields.Date(default=fields.Date.context_today, required=True,
                                  help="Fecha")

    @api.model
    def create(self, vals):
        seq = self.env['ir.sequence'].next_by_code('bi.peso.uniformidad') or '/'
        vals['name'] = seq
        return super(BiPesoUniformidad, self).create(vals)





   



