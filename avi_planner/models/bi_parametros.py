# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import fields, models, api

class BiClasificacionHuevo(models.Model):
    _name="bi.clasificacion.huevo"
    _inherit = ['mail.thread']
    _description="Clasificacion Huevo"

    name=fields.Char(string="Clasificacion de Huevo")

#Parametros
class BiParametros(models.Model):
    _name="bi.parametros"
    _inherit = ['mail.thread']
    _description="Parametros Mortalidad, Produccion, Consumos"

    def _get_tipo_granja(self):
       return self.env['bi.granja.tipo'].search([], limit=1)
    def _get_alimento(self):
        return self.env['bi.alimento'].search([], limit=1)
    def _get_clasificaciones(self):
        return self.env['bi.clasificacion.huevo'].search([], limit=1)
    def _get_dia_edad(self):
        return self.env['bi.dia.edad.parametro'].search([],limit=1)
    def _get_raza(self):
        return self.env['bi.raza'].search([], limit=1)
    tipo_granja_id = fields.Many2one(
        comodel_name='bi.granja.tipo', string="Tipo de Granja", default=_get_tipo_granja, required=True)
    raza_id = fields.Many2one(
        comodel_name='bi.raza', string="Raza", default=_get_raza, required=True)
    #parametros de crianza
    crianza_edad_dia_inicio = fields.Integer(string="Dia Inicio")
    crianza_edad_dia_fin = fields.Integer(string="Dia Finaliza")
    crianza_edad_semana = fields.Integer(string="Semana Edad Crianza")
    crianza_meta_peso_corporal = fields.Float(string="Peso Corporal Meta")
    crianza_meta_uniformidad = fields.Float(string="Uniformidad")
    crianza_meta_mortalidad = fields.Float(string="Porcenta de Mortalidad Meta")
    crianza_meta_mortalidad_acum = fields.Float(string="Mortalidad Acumulada %")
    crianza_meta_cons_alim_grs = fields.Float(string="Consumo de Alimento (GRS)")
    crianza_meta_cons_alim_acum_grs = fields.Float(string="Consumo de Alimento Acumulado (GRS)")


    #parametros de postura
    postura_edad_semana = fields.Integer(string="Semana Edad Postura")
    postura_edad = fields.Integer(string="Postura Edad ave")
    postura_prodAve = fields.Float(string="Postura % Produccion ave")
    postura_viabilidad = fields.Float(string="Postura % Viabilidad")
    postura_meta_mortalidad = fields.Float(string="Postura % de mortalidad")
    postura_meta_mortalidad_acum = fields.Float(string="Postura % Mortalidad acumulada")
    postura_meta_sucio = fields.Float(string="Postura % Huevo Sucio")
    postura_meta_cascado = fields.Float(string="Postura % Huevo Cascado")
    postura_meta_huevo_acumulado_ave = fields.Float(string="Postura Huevo acumulado por ave")
    postura_meta_peso_prom_huevo_gramos = fields.Float(string="Postura Peso promedio de huevo en gramos")
    postura_meta_masa_huevo_dia = fields.Float(string="Postura Masa de huevo al dia")
    postura_meta_masa_huevo_acum_ave = fields.Float(string="Postura Masa de huevo acumulado por ave")
    postura_meta_cons_alim_ave_dia = fields.Float(string="Postura Consumo de alimento por ave al dia")
    postura_meta_cons_alim_acum_ave_dia = fields.Float(string="Postura Consumo acumulado de alimento por ave al dia")
    postura_peso_corporal = fields.Float(string="Postura Peso corporal del ave")
    
    #TODO: En la base de datos originalmente es tipoAlimento
    alimento_id = fields.Many2one(comodel_name='bi.alimento', string="Alimento", default=_get_alimento, required=True)
    clasificacion_id = fields.Many2one(comodel_name='bi.clasificacion.huevo', string="Clasificacion Huevo", default=_get_clasificaciones)
