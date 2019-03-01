# -*- coding: utf-8 -*-

from odoo import fields, models, api

#TOLVA
class BiTolva(models.Model):
    _name = 'bi.tolva'
    _inherit = ['mail.thread']
    _description = 'Tolvas de granjas'


    def _get_granja(self):
        return self.env['bi.granja'].search([], limit=1)

    name = fields.Char(string='Numero', required=True)
    caseta_id = fields.Many2one(comodel_name='bi.granja.caseta', string="Caseta")
    granja_id = fields.Many2one(comodel_name='bi.granja',default=_get_granja, string="Granja")
    capacidad = fields.Float(string="Capacidad Kgs")
    #alimento_existente = fields.Integer(string="Kgs. Exitentes", compute="_compute_alimento_existente")

'''
    @api.multi
    @api.depends('alimento_existente')
    def _compute_alimento_existente(self):
        for r in self:
            #entradas de alimento
            entradas_objs = self.env['bi.registro.alimento'].search([('tipo_evento_id','=',1),('granja_id','=',r.granja_seccion_caseta_id.id),('tolva_id','=',r.id),('state','=','finished')])
            suma_entradas=0
            alimento=0
            for e in entradas_objs:
                suma_entradas += e.kgs_entrada
                alimento = e.alimento_id

            #consumos de alimento
            suma_consumos = 0
            consumos_objs = self.env['bi.registro.alimento'].search([('tipo_evento_id','=',2),('granja_id','=',r.granja_seccion_caseta_id.id),('tolva_id','=',r.id),('state','=','finished')])
            for c in consumos_objs:
                suma_consumos += c.consumo

            #traspaso de alimento a favor
            suma_traspaso_favor = 0
            traspaso_favor_objs = self.env['bi.registro.alimento'].search([('tipo_evento_id','=',3),('granja_destino_id','=',r.granja_seccion_caseta_id.id),('tolva_destino_id','=',r.id),('state','=','finished')])
            for t in traspaso_favor_objs:
                suma_traspaso_favor += t.kgs_traspaso

            #traspaso de alimento en contra
            traspaso_contra_objs = self.env['bi.registro.alimento'].search([('tipo_evento_id','=',3),('granja_id','=',r.granja_seccion_caseta_id.id),('tolva_id','=',r.id),('state','=','finished')])
            suma_traspaso_contra = 0
            for tc in traspaso_contra_objs:
                suma_traspaso_contra += tc.kgs_traspaso


            r.alimento_existente = (suma_entradas + suma_traspaso_favor) - (suma_consumos + suma_traspaso_contra)
            r.alimento_id = alimento


    #valorx = fields.Float(string="Valor X")
    #vacio_uno = fields.Float(string="Vacio 1")
    #vacio_dos = fields.Float(string="Vacio 2")
    #vacio_tres = fields.Float(string="Vacio 3")
    #vacio_total = fields.Float(string="Vacio Total")
    #m_uno = fields.Float(string="M1")
    #m_dos = fields.Float(string="M2")
    #m_tres = fields.Float(string="M3")
    #m_total = fields.Float(string="M Total")
    state = fields.Boolean(string="Estado")
'''

#CONFIGURACION DE TOLVA
class BiConfigTolva(models.Model):
    _name ='bi.tolva.config'
    _inherit = ['mail.thread']
    _description = 'Configuracion de tolvas'

    #parametro_1 = fields.Float(string="Parametro 1")
    def _get_granja(self):
        return self.env['bi.granja'].search([], limit=1)

    granja_id = fields.Many2one(
        comodel_name='bi.granja', string="Granja", default=_get_granja, required=True)






   



