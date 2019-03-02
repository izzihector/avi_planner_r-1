# -*- coding: utf-8 -*-
#************************** 
# @author: Ivan Porras
#**************************

from odoo import fields, models, api

class BiProduccion(models.Model):
    _name = 'bi.produccion'
    _inherit = ['mail.thread']
    _description = 'Produccion de huevo'

    #para la secuencia
    name = fields.Char('Nombre', readonly=True)

    def _get_granja(self):
      return self.env['bi.granja'].search([('tipo_granja_id.name','=','POSTURA')], limit=1)
    def _get_marca(self):
      return self.env['bi.marca'].search([], limit=1)

    fecha= fields.Date(default=fields.Date.context_today)  
    granja_id = fields.Many2one(comodel_name='bi.granja', string="Granja", default=_get_granja, required=True)
    tipo_granja = fields.Char(related='granja_id.tipo_granja_id.name',readonly=True)
    marca_id= fields.Many2one(comodel_name='bi.marca', string="Marca", default=_get_marca, required=True)
    marca = fields.Char(related='marca_id.name',readonly=True)

    
    caja_360_chico = fields.Integer(string="Caja 360 Chico")#SACAMECATE
    caja_360 = fields.Integer(string="Caja 360 Linea")#SACAMECATE

    #TODO: Quitar este campo de la vista, preguntar para que sirve: 
    sobra_pz_360 = fields.Integer(string="")#SACAMECATE

    
    caja_jumbo = fields.Integer(string="Piezas Jumbo")#SACAMECATEA 
    caja_180 = fields.Integer(string="Caja 180 Media")#SACAMECATE
    
    
    pza_sucio = fields.Integer(string="Piezas Sucio")
    pza_cascado = fields.Integer(string="Piezas Cascado")
    pza_deforme = fields.Integer(string="Piezas Deforme")

    #TODO: Quitar este campo de los formularios y preguntar para que sirven
    caja_roto = fields.Integer(string="Caja Roto")

    
    bolsa_desyemado = fields.Integer(string="Bolsa Desyemado Piezas",help="Piezas de Huevo")

    #TODO: Preguntar donde poner estos campos
    caja_12_nero = fields.Integer(string="Caja 12 Nero")
    caja_18_nero = fields.Integer(string="Caja 18 Nero")
    
    #TODO: Preguntar para que son estos campos
    cinta_total = fields.Integer(string="Cinta Total")
    cinta_sobra = fields.Integer(string="Cinta Sobra")

    # secuencia de produccion
    @api.model
    def create(self, vals):
        seq = self.env['ir.sequence'].next_by_code('bi.produccion') or '/'
        vals['name'] = seq
        return super(BiProduccion, self).create(vals)

    #Acciones de Status
    @api.one
    def cancel_progressbar(self):
        self.write({
            'state':'cancel'
        })



class BiMarca(models.Model):
    _name="bi.marca"
    _inherit = ['mail.thread']
    _description="Marca"

    name=fields.Char(string="Marca")

