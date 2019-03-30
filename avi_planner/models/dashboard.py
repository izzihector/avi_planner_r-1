from odoo import fields, models, api


class AviplannerDashboard(models.Model):
    _name = "avi.dashboard"

    name = fields.Char(string="")

    granja_id = fields.Many2one(comodel_name='bi.granja', string="Granja")
    parvada_id = fields.Many2one(comodel_name='bi.parvada', string="# Parvada")

    @api.model
    def get_granjas_info(self):
        return self.env['bi.granja'].search([])
