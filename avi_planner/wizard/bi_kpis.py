# -*- coding: utf-8 -*-
# @author: Ivan Porras
from bokeh.plotting import figure
from bokeh.models import HoverTool
from bokeh.embed import components

from odoo import api, fields, models
import logging


logger = logging.getLogger(__name__)


class BiKpiMortalidad(models.TransientModel):
    _name = 'bi.crianza.kpi.mortalidad'
    _description = 'KPI de mortalidad en crianza'

    def _get_granja(self):
        return self.env['bi.granja'].search([], limit=1)

    dias_edad_ave = fields.Integer(string="Dias edad ave")
    semena_edad_ave = fields.Integer(string="Semana Edad Ave")
    granja = fields.Char(string="Granja")
    caseta = fields.Char(string="Caseta")
    mortalidad_porcen = fields.Float(string="% Mortalidad Real")
    mortalidad_porcen_meta = fields.Float(string="% Mortalidad Meta")
    mortalidad_porcen_acum = fields.Float(string="% Mortalidad Acum")
    mortalidad_porcen_acum_meta = fields.Float(string="% Mortalidad Acum Meta")
    consumo_alimento_grs_ave = fields.Float(string="Consumo alimento GRS Ave")
    consumo_alimento_grs_ave_meta = fields.Float(string="Consumo alimento GRS Ave Meta")
    consumo_alimento_grs_ave_acum = fields.Float(string="Consumo alimento GRS Ave Acumulado Real")
    consumo_alimento_grs_ave_acum_meta = fields.Float(string="Consumo alimento GRS Ave Acumulado Meta")



class BiReporteo(models.TransientModel):
    _name = 'bi.wizard.kpi'

    def _get_granja(self):
        return self.env['bi.granja'].search([], limit=1)
    def _get_parvada(self):
        return self.env['bi.parvada'].search([], limit=1)

    def _compute_bokeh_chart(self):
        for rec in self:
            x = []
            y1 = []
            y2 = []
            mortalidad = rec.env['bi.crianza.kpi.mortalidad'].search([])
            if rec.periodo == 'semana': ############################################## by week
                if self.indicador == 'mortalidad_porcentaje':
                    for m in mortalidad:
                        x.append(m.semena_edad_ave)
                        y1.append(round(m.mortalidad_porcen,2))
                        y2.append(round(m.mortalidad_porcen_meta,2))
                elif self.indicador == 'mortalidad_porcentaje_acum':
                    for m in mortalidad:
                        x.append(m.semena_edad_ave)
                        y1.append(m.mortalidad_porcen_acum)
                        y2.append(m.mortalidad_porcen_acum_meta)
                elif self.indicador == 'consumo_grs_ave':
                    for m in mortalidad:
                        x.append(m.semena_edad_ave)
                        y1.append(m.consumo_alimento_grs_ave)
                        y2.append(m.consumo_alimento_grs_ave_meta)
                elif self.indicador == 'consumo_grs_ave_acum':
                    for m in mortalidad:
                        x.append(m.semena_edad_ave)
                        y1.append(m.consumo_alimento_grs_ave_acum)
                        y2.append(m.consumo_alimento_grs_ave_acum_meta)
            elif rec.periodo == 'dia': ################################################ by day
                if self.indicador == 'mortalidad_porcentaje':
                    for m in mortalidad:
                        x.append(m.dias_edad_ave)
                        y1.append(m.mortalidad_porcen)
                        y2.append(m.mortalidad_porcen_meta)
                elif self.indicador == 'mortalidad_porcentaje_acum':
                    for m in mortalidad:
                        x.append(m.dias_edad_ave)
                        y1.append(m.mortalidad_porcen_acum)
                        y2.append(m.mortalidad_porcen_acum_meta)
                elif self.indicador == 'consumo_grs_ave':
                    for m in mortalidad:
                        x.append(m.dias_edad_ave)
                        y1.append(m.consumo_alimento_grs_ave)
                        y2.append(m.consumo_alimento_grs_ave_meta)
                elif self.indicador == 'consumo_grs_ave_acum':
                    for m in mortalidad:
                        x.append(m.dias_edad_ave)
                        y1.append(m.consumo_alimento_grs_ave_acum)
                        y2.append(m.consumo_alimento_grs_ave_acum_meta)

            #conceptos para imprimir en grafica
            title = ""
            x_axis_label = ""
            y_axis_label = ""
            legend1 = ""
            legend2 = ""

            hover = HoverTool()
            if self.indicador == 'mortalidad_porcentaje':
                title = "Mortalidad por "+ rec.periodo
                x_axis_label =""+rec.periodo+" "+"edad"
                y_axis_label ="% mortalidad"
                legend1 ="% Mortalidad Real"
                legend2 ="% Mortalidad Meta"
                hover.tooltips = [
                    (rec.periodo+" "+"edad", "@x"),
                    (y_axis_label, "@y{0.0000}%"),
                ]
            elif self.indicador == 'mortalidad_porcentaje_acum':
                title = "Mortalidad Acumulada por " + rec.periodo
                x_axis_label = "" + rec.periodo + " " + "edad"
                y_axis_label = "% Mortalidad Acum"
                legend1 = "% Mortalidad Real Acum"
                legend2 = "% Mortalidad Meta Acum"
                hover.tooltips = [
                    (rec.periodo + " " + "edad", "@x"),
                    (y_axis_label, "@y{0.0000}%"),
                ]
            elif self.indicador == 'consumo_grs_ave':
                title = "Consumo alimento ave por " + rec.periodo
                x_axis_label = "" + rec.periodo + " " + "edad"
                y_axis_label = "GRS Consumo Ave"
                legend1 = "Consumo grs. Real"
                legend2 = "Consumo grs. Meta"
                hover.tooltips = [
                    (rec.periodo + " " + "edad", "@x"),
                    (y_axis_label, "@y{0.0000}"),
                ]
            elif self.indicador == 'consumo_grs_ave_acum':
                title = "Consumo alimento ave acumulado por " + rec.periodo
                x_axis_label = "" + rec.periodo + " " + "edad"
                y_axis_label = "GRS Consumo Ave Acum"
                legend1 = "Consumo grs. Real Acum"
                legend2 = "Consumo grs. Meta Acum"
                hover.tooltips = [
                    (rec.periodo + " " + "edad", "@x"),
                    (y_axis_label, "@y{0.0000}"),
                ]

            # Get the html components and convert them to string into the fiel

            p = figure(
                tools="pan,box_zoom,reset,save", title=title,
                x_axis_label=x_axis_label, y_axis_label=y_axis_label,
                plot_width=1100, plot_height=600
            )

            p.tools.append(hover)

            p.line(x, y1, legend=legend1, line_color="red")
            p.circle(x, y1, legend=legend1, fill_color="red", line_color="red", size=6)
            p.line(x, y2, legend=legend2)
            p.circle(x, y2, legend=legend2, fill_color="white", size=8)

            script, div = components(p)
            rec.bokeh_chart = '%s%s' % (div, script)

    bokeh_chart = fields.Text(
        string='Bokeh Chart',
        compute=_compute_bokeh_chart)

    filtros = fields.Selection([('a',''),('granja_parvada', 'Granja / Parvada'), ('granja_caseta', 'Granja / Caseta')],default='a')
    caseta_id = fields.Many2one(comodel_name='bi.granja.caseta', string="Caseta")
    granja_id = fields.Many2one(comodel_name='bi.granja', default=_get_granja, string="Granja")
    parvada_id = fields.Many2one(comodel_name='bi.parvada',string="# Parvada", default=_get_parvada)
    periodo = fields.Selection([('dia','Dia'),('semana', 'Semana')])
    semana = fields.Selection([('sem1', '1'), ('sem2', '2'), ('sem3', '3'), ('sem4', '4'), ('sem5', '5'),
                               ('sem6', '6'), ('sem7', '7'), ('sem8', '8'), ('sem9', '9'), ('sem10', '10'),
                               ('sem11', '11'), ('sem12', '12'), ('sem13', '13'), ('sem14', '14'),
                               ('sem15', '15'), ('sem16', '16'), ('sem17', '17'), ('sem18', '18')])

    mes = fields.Selection([('enero', 'Enero'), ('febrero', 'Febrero'), ('marzo', 'Marzo'), ('abril', 'Abril')
                               , ('mayo', 'Mayo'), ('junio', 'Junio'), ('julio', 'Julio'), ('agosto', 'Agosto'),
                            ('septiembre', 'Septiembre'), ('octubre', 'Octubre'), ('noviembre', 'Noviembre'),
                            ('diciembre', 'Diciembre')])

    indicador = fields.Selection([('consumo_grs_ave_acum','Consumo Gramos Ave Acumulado'),('consumo_grs_ave', 'Consumo Gramos Ave'),
                                  ('mortalidad_porcentaje', '% Mortalidad'),
                                  ('mortalidad_porcentaje_acum', '% Mortalidad Acumulada')])

    @api.multi
    def action_view_lines(self):
        self.bokeh_chart = "";
        self.env['bi.crianza.kpi.mortalidad'].search([]).unlink()
        self.ensure_one()
        self._compute_data()
        self._compute_bokeh_chart()
        return {
            'view_type': 'form',
            'view_mode': 'tree,form,graph',
            'res_model': 'bi.crianza.kpi.mortalidad',
            'type': 'ir.actions.act_window',
            'domain': "[]",
            'target': 'new',
        }

    @api.multi
    def action_view_graph(self):
        self.bokeh_chart = "";
        self.env['bi.crianza.kpi.mortalidad'].search([]).unlink()
        self.ensure_one()
        self._compute_data()
        self._compute_bokeh_chart()
        return {
            'view_type': 'form',
            'view_mode': 'tree,form,graph',
            'res_model': 'bi.crianza.kpi.mortalidad',
            'type': 'ir.actions.client',
            'domain': "[]",
            'tag': 'reload',
        }

    def _compute_data(self):
        self._sql_report_object()
        self._sql_insert_mortalidad()

    def _sql_report_object(self):
        if self.filtros == 'granja_caseta':
            query_funcion = """ 

CREATE OR REPLACE FUNCTION public.balanza_aves(IN x_caseta_id integer)
  RETURNS TABLE(fecha date, semana_year character varying, semana_edad_ave numeric, dias_edad_ave numeric, granja character varying, seccion character varying, caseta character varying, poblacion_inicial numeric, entradas numeric, mortalidad numeric, porcentaje_mortalidad numeric, 
  meta_porcentaje_mortalidad numeric, 
  mortalidad_acum numeric, porcentaje_mortalidad_acum numeric, meta_mortalidad_acum numeric, 
  poblacion_final numeric, consumo_alimento_kgs_total numeric, consumo_alimento_grs_ave numeric, 
  consumo_alimento_grs_ave_meta numeric,
  consumo_alimento_grs_ave_acum numeric,
  consumo_alimento_grs_ave_acum_meta numeric) AS
$BODY$
        DECLARE
          _parvada_id numeric;
          _fecha_primer_recepcion date;
          _fecha_ultima_recepcion date;
          _dias_diff_fechas numeric;
          _fecha_inicial_edad_ave date;
          _dias_edad_ave numeric;
          _semana_edad_ave numeric;
          _semana_year character varying;
          _granja varchar;
          _seccion varchar;
          _caseta varchar;
          _poblacion_inicial numeric;
          _entradas numeric;
          _mortalidad numeric;  
          _porcentaje_mortalidad numeric(4,4);
          _meta_porcentaje_mortalidad numeric(4,4); --- META
          _mortalidad_acum numeric;
          _meta_mortalidad_acum numeric;
          _porcentaje_mortalidad_acum numeric(4,2);
          _poblacion_final numeric;
          _total_recepciones numeric; 
          _fecha_inicio_cursor date;
          _fecha_finaliza_curos date;
          
          r record;
          c CURSOR FOR  select date(dd.dd) as Fecha from 
			generate_series (_fecha_inicio_cursor ::timestamp,(select now())::timestamp, '1 day'::interval) dd;

	  --- ALIMENTO
	  _consumo_alimento_kgs_total numeric;
	  _consumo_alimento_grs_ave numeric;
	  _consumo_alimento_grs_ave_meta numeric;
	  _consumo_alimento_grs_ave_acum numeric;
	  _consumo_alimento_grs_ave_acum_meta numeric;
        BEGIN
          DROP TABLE IF EXISTS BALANZA_AVES;
          CREATE TEMP TABLE BALANZA_AVES (fecha date,
                          semana_year character varying,
                          semana_edad_ave numeric,
                          dias_edad_ave numeric,
                          granja varchar, 
                          seccion varchar, 
                          caseta varchar, 
                          poblacion_inicial  numeric, 
                          entradas numeric, 
                          mortalidad numeric,
                          porcentaje_mortalidad numeric(5,5),
                          meta_porcentaje_mortalidad numeric(5,5),
                          mortalidad_acum numeric, 
                          meta_mortalidad_acum numeric, ---META MORTALIDA ACUM
                          porcentaje_mortalidad_acum numeric(4,2), 
                          poblacion_final  numeric,
                          consumo_alimento_kgs_total numeric,
                          consumo_alimento_grs_ave numeric,
                          consumo_alimento_grs_ave_meta numeric,
                          consumo_alimento_grs_ave_acum numeric,
                          consumo_alimento_grs_ave_acum_meta numeric);

	   _parvada_id := (select parvada_id from bi_granja_caseta where id = x_caseta_id);
	  _fecha_inicio_cursor := (select fecha_recepcion from bi_parvada_recepcion bpr where parvada_id = _parvada_id and bpr.caseta_id = x_caseta_id order by fecha_recepcion asc limit 1);
	  
          FOR r IN c LOOP
            -- Para obtener la edad de la parvada
            _fecha_primer_recepcion := (select fecha_recepcion from bi_parvada_recepcion bpr where parvada_id = _parvada_id and bpr.caseta_id = x_caseta_id order by fecha_recepcion asc limit 1);
            _fecha_ultima_recepcion := (select fecha_recepcion from bi_parvada_recepcion bpr where parvada_id = _parvada_id and bpr.caseta_id = x_caseta_id order by fecha_recepcion desc limit 1);	
            _dias_diff_fechas := (date_part('day',age(_fecha_ultima_recepcion, _fecha_primer_recepcion)))/2;
            _fecha_inicial_edad_ave := _fecha_primer_recepcion + interval '1 days';
            _dias_edad_ave := (select r.fecha::date - _fecha_primer_recepcion::date);
            _semana_edad_ave:= ((select r.fecha::date -  _fecha_primer_recepcion::date)/7);

            RAISE NOTICE 'Fecha actual  % y fecha recepcion % y dia %',r.fecha,_fecha_primer_recepcion,(select date_part('day', age(r.fecha, _fecha_primer_recepcion)));
                
            --granja
            _granja := (select ga.name from bi_granja_caseta ca inner join bi_granja ga on ga.id = ca.granja_id where ca.id = x_caseta_id);	 
            --seccion
            _seccion := (select s.name from bi_granja_caseta ca inner join bi_granja_seccion s on s.id = ca.seccion_id where ca.id = x_caseta_id);  
            --caseta
            _caseta := (select ca.name from bi_granja_caseta ca where ca.id = x_caseta_id);  
            --poblacion inicial
            _poblacion_inicial := (select BA.poblacion_final from BALANZA_AVES BA where BA.fecha = (r.fecha - interval '1 day'));
            --entradas
            _entradas:= (select COALESCE(sum(bpr.poblacion_entrante),0) from bi_parvada_recepcion bpr where bpr.fecha_recepcion = r.fecha and bpr.caseta_id = x_caseta_id and bpr.parvada_id = _parvada_id); 
            --mortalidad
            _mortalidad := (select COALESCE(sum(causa_seleccion),0) + COALESCE(sum(causa_paralitica),0) + COALESCE(sum(causa_natural),0) + COALESCE(sum(causa_sacrificada),0) from bi_parvada_mortalidad bpm where bpm.fecha = r.fecha and  bpm.caseta_id = x_caseta_id and bpm.parvada_id = _parvada_id);
            --porcentaje de mortalidad
            _porcentaje_mortalidad := CASE WHEN _poblacion_inicial = 0 then 0.00000 ELSE COALESCE(_mortalidad,0) / COALESCE(_poblacion_inicial,1)*100 END;
            _meta_porcentaje_mortalidad := (select crianza_meta_mortalidad from bi_parametros where crianza_edad_semana = round(_semana_edad_ave,0));
            --mortalidad acumulado
            _mortalidad_acum := COALESCE((select BA.mortalidad_acum from BALANZA_AVES BA where BA.fecha = (r.fecha - interval '1 day')),0) + _mortalidad;            			    
            _meta_mortalidad_acum := (select crianza_meta_mortalidad_acum from bi_parametros where crianza_edad_semana = round(_semana_edad_ave,0));
            --poblacion final
            _poblacion_final := COALESCE(_poblacion_inicial,0) + COALESCE(_entradas,0) - COALESCE(_mortalidad,0); 
            --semana del año
            _semana_year := (SELECT date_part('week',r.fecha));
            --total de recepciones en la caseta
            _total_recepciones:= (select COALESCE(sum(bpr.poblacion_entrante),0) from bi_parvada_recepcion bpr where bpr.caseta_id = x_caseta_id); 
             --porcentaje de mortalidad acumulado
            _porcentaje_mortalidad_acum := CASE WHEN _total_recepciones = 0 then 0.00000 ELSE COALESCE(_mortalidad_acum,0) / COALESCE(_total_recepciones,1)*100 END;

	    ----- ALIMENTO CONSUMIDO-----------------------------
	    _consumo_alimento_kgs_total := (SELECT COALESCE(sum(consumo),0) FROM public.bi_registro_alimento bra 
	                          where bra.fecha = r.fecha and bra.tipo_evento_id = 2 and bra.state= 'finished' and bra.parvada_id = _parvada_id and bra.caseta_id = x_caseta_id) ;
	    
	    _consumo_alimento_grs_ave := (_consumo_alimento_kgs_total *1000) / _poblacion_inicial;
	    _consumo_alimento_grs_ave_meta := (select crianza_meta_cons_alim_grs from bi_parametros where crianza_edad_semana = round(_semana_edad_ave,0));
	    _consumo_alimento_grs_ave_acum := COALESCE((select BA.consumo_alimento_grs_ave_acum from BALANZA_AVES BA where BA.fecha = (r.fecha - interval '1 day')),0) + _consumo_alimento_grs_ave;
            _consumo_alimento_grs_ave_acum_meta := (select crianza_meta_cons_alim_acum_grs from bi_parametros where crianza_edad_semana = round(_semana_edad_ave,0));
            INSERT INTO BALANZA_AVES VALUES(
                             r.fecha,
                            _semana_year,
                           _semana_edad_ave,
                            _dias_edad_ave,
                            _granja,
                            _seccion,_caseta,
                            _poblacion_inicial,
                            _entradas,
                            _mortalidad,
                            _porcentaje_mortalidad,
                            _meta_porcentaje_mortalidad,
                            _mortalidad_acum,                            
                            _porcentaje_mortalidad_acum,
                            _meta_mortalidad_acum,
                            _poblacion_final,
                            _consumo_alimento_kgs_total,
                            _consumo_alimento_grs_ave,
                            _consumo_alimento_grs_ave_meta,
                            _consumo_alimento_grs_ave_acum,
                            _consumo_alimento_grs_ave_acum_meta);
          END LOOP;  
          RETURN QUERY SELECT * FROM BALANZA_AVES;
          
        END;
        $BODY$
  LANGUAGE plpgsql VOLATILE
         """
            self.env.cr.execute(query_funcion)
        elif self.filtros == 'granja_parvada':
            query_funcion_parvada = """
            CREATE OR REPLACE FUNCTION public.balanza_aves_parvada(IN x_granja_id integer,IN x_parvada_id integer)
  RETURNS TABLE(fecha date, semana_year character varying, semana_edad_ave numeric, dias_edad_ave numeric, granja character varying,poblacion_inicial numeric, entradas numeric, mortalidad numeric, porcentaje_mortalidad numeric, meta_porcentaje_mortalidad numeric, mortalidad_acum numeric, porcentaje_mortalidad_acum numeric, meta_mortalidad_acum numeric, poblacion_final numeric, consumo_alimento_kgs_total numeric, consumo_alimento_grs_ave numeric, consumo_alimento_grs_ave_meta numeric, consumo_alimento_grs_ave_acum numeric, consumo_alimento_grs_ave_acum_meta numeric) AS
$BODY$
        DECLARE
          _parvada_id numeric;
          _fecha_primer_recepcion date;
          _fecha_ultima_recepcion date;
          _dias_diff_fechas numeric;
          _fecha_inicial_edad_ave date;
          _dias_edad_ave numeric;
          _semana_edad_ave numeric;
          _semana_year character varying;
          _granja varchar;
          _poblacion_inicial numeric;
          _entradas numeric;
          _mortalidad numeric;  
          _porcentaje_mortalidad numeric(4,4);
          _meta_porcentaje_mortalidad numeric(4,4); --- META
          _mortalidad_acum numeric;
          _meta_mortalidad_acum numeric;
          _porcentaje_mortalidad_acum numeric(4,2);
          _poblacion_final numeric;
          _total_recepciones numeric; 
          _fecha_inicio_cursor date;
          _fecha_finaliza_curos date;
          
          r record;
          c CURSOR FOR  select date(dd.dd) as Fecha from 
			generate_series (_fecha_inicio_cursor ::timestamp,(select now())::timestamp, '1 day'::interval) dd;

	  --- ALIMENTO
	  _consumo_alimento_kgs_total numeric;
	  _consumo_alimento_grs_ave numeric;
	  _consumo_alimento_grs_ave_meta numeric;
	  _consumo_alimento_grs_ave_acum numeric;
	  _consumo_alimento_grs_ave_acum_meta numeric;
        BEGIN
          DROP TABLE IF EXISTS BALANZA_AVES;
          CREATE TEMP TABLE BALANZA_AVES (fecha date,
                          semana_year character varying,
                          semana_edad_ave numeric,
                          dias_edad_ave numeric,
                          granja varchar, 
                          poblacion_inicial  numeric, 
                          entradas numeric, 
                          mortalidad numeric,
                          porcentaje_mortalidad numeric(5,5),
                          meta_porcentaje_mortalidad numeric(5,5),
                          mortalidad_acum numeric, 
                          meta_mortalidad_acum numeric,
                          porcentaje_mortalidad_acum numeric(4,2), 
                          poblacion_final  numeric,
                          consumo_alimento_kgs_total numeric,
                          consumo_alimento_grs_ave numeric,
                          consumo_alimento_grs_ave_meta numeric,
                          consumo_alimento_grs_ave_acum numeric,
                          consumo_alimento_grs_ave_acum_meta numeric);


	  _fecha_inicio_cursor := (select fecha_recepcion from bi_parvada_recepcion bpr where parvada_id = x_parvada_id and granja_id = x_granja_id order by fecha_recepcion asc limit 1);
	  IF _fecha_inicio_cursor  is not null
	  THEN
		  FOR r IN c LOOP
		    -- Para obtener la edad de la parvada
		    _fecha_primer_recepcion := (select fecha_recepcion from bi_parvada_recepcion bpr where parvada_id = x_parvada_id and granja_id = x_granja_id order by fecha_recepcion asc limit 1);
		    _fecha_ultima_recepcion := (select fecha_recepcion from bi_parvada_recepcion bpr where parvada_id = x_parvada_id and granja_id = x_granja_id order by fecha_recepcion desc limit 1);	
		    _dias_diff_fechas := (date_part('day',age(_fecha_ultima_recepcion, _fecha_primer_recepcion)))/2;
		    _fecha_inicial_edad_ave := _fecha_primer_recepcion + interval '1 days';
		    _dias_edad_ave := (select r.fecha::date - _fecha_primer_recepcion::date);
		    _semana_edad_ave:= ((select r.fecha::date -  _fecha_primer_recepcion::date)/7);

		    RAISE NOTICE 'Fecha actual  % y fecha recepcion % y dia %',r.fecha,_fecha_primer_recepcion,(select date_part('day', age(r.fecha, _fecha_primer_recepcion)));
			
		    --granja
		    _granja := (select ga.name from bi_granja ga where ga.id = x_granja_id);	 
		    --poblacion inicial
		    _poblacion_inicial := (select BA.poblacion_final from BALANZA_AVES BA where BA.fecha = (r.fecha - interval '1 day'));
		    --entradas
		    _entradas:= (select COALESCE(sum(bpr.poblacion_entrante),0) from bi_parvada_recepcion bpr where bpr.fecha_recepcion = r.fecha and bpr.parvada_id = x_parvada_id and bpr.granja_id = x_granja_id); 
		    --mortalidad
		    _mortalidad := (select COALESCE(sum(causa_seleccion),0) + COALESCE(sum(causa_paralitica),0) + COALESCE(sum(causa_natural),0) + COALESCE(sum(causa_sacrificada),0) from bi_parvada_mortalidad bpm where bpm.fecha = r.fecha and bpm.parvada_id = x_parvada_id 
				    and bpm.granja_id = x_granja_id);
		    --porcentaje de mortalidad
		    _porcentaje_mortalidad := CASE WHEN _poblacion_inicial = 0 then 0.00000 ELSE COALESCE(_mortalidad,0) / COALESCE(_poblacion_inicial,1)*100 END;
		    _meta_porcentaje_mortalidad := (select crianza_meta_mortalidad from bi_parametros where crianza_edad_semana = round(_semana_edad_ave,0));
		    --mortalidad acumulado
		    _mortalidad_acum := COALESCE((select BA.mortalidad_acum from BALANZA_AVES BA where BA.fecha = (r.fecha - interval '1 day')),0) + _mortalidad;            			    
		    _meta_mortalidad_acum := (select crianza_meta_mortalidad_acum from bi_parametros where crianza_edad_semana = round(_semana_edad_ave,0));
		    --poblacion final
		    _poblacion_final := COALESCE(_poblacion_inicial,0) + COALESCE(_entradas,0) - COALESCE(_mortalidad,0); 
		    --semana del año
		    _semana_year := (SELECT date_part('week',r.fecha));
		    --total de recepciones en la caseta
		    _total_recepciones:= (select COALESCE(sum(bpr.poblacion_entrante),0) from bi_parvada_recepcion bpr where bpr.parvada_id = x_parvada_id and bpr.granja_id = x_granja_id); 
		     --porcentaje de mortalidad acumulado
		    _porcentaje_mortalidad_acum := CASE WHEN _total_recepciones = 0 then 0.00000 ELSE COALESCE(_mortalidad_acum,0) / COALESCE(_total_recepciones,1)*100 END;

		    _consumo_alimento_kgs_total := (SELECT COALESCE(sum(consumo),0) FROM public.bi_registro_alimento bra 
					  where bra.fecha = r.fecha and bra.tipo_evento_id = 2 and bra.state= 'finished' and bra.parvada_id = x_parvada_id and bra.parvada_id = x_granja_id) ;
		    
		    _consumo_alimento_grs_ave := (_consumo_alimento_kgs_total *1000) / _poblacion_inicial;
		    _consumo_alimento_grs_ave_meta := (select crianza_meta_cons_alim_grs from bi_parametros where crianza_edad_semana = round(_semana_edad_ave,0));
		    _consumo_alimento_grs_ave_acum := COALESCE((select BA.consumo_alimento_grs_ave_acum from BALANZA_AVES BA where BA.fecha = (r.fecha - interval '1 day')),0) + _consumo_alimento_grs_ave;
		    _consumo_alimento_grs_ave_acum_meta := (select crianza_meta_cons_alim_acum_grs from bi_parametros where crianza_edad_semana = round(_semana_edad_ave,0));
		    INSERT INTO BALANZA_AVES VALUES(
				     r.fecha,
				    _semana_year,
				   _semana_edad_ave,
				    _dias_edad_ave,
				    _granja,
				    _poblacion_inicial,
				    _entradas,
				    _mortalidad,
				    _porcentaje_mortalidad,
				    _meta_porcentaje_mortalidad,
				    _mortalidad_acum,                            
				    _porcentaje_mortalidad_acum,
				    _meta_mortalidad_acum,
				    _poblacion_final,
				    _consumo_alimento_kgs_total,
				    _consumo_alimento_grs_ave,
				    _consumo_alimento_grs_ave_meta,
				    _consumo_alimento_grs_ave_acum,
				    _consumo_alimento_grs_ave_acum_meta);
		  END LOOP;  
	  END IF;
          RETURN QUERY SELECT * FROM BALANZA_AVES;
          
        END;
        $BODY$
  LANGUAGE plpgsql VOLATILE
            """
            self.env.cr.execute(query_funcion_parvada)

    def _sql_insert_mortalidad(self):
        query=""
        query_parvada=""
        if self.periodo == 'semana':
            if self.indicador == 'mortalidad_porcentaje':
                if self.filtros == 'granja_caseta':
                    query =""" INSERT INTO bi_crianza_kpi_mortalidad(
                               granja,
                               caseta,
                               semena_edad_ave,
                               mortalidad_porcen,
                               mortalidad_porcen_meta)                      
                               SELECT GRANJA,CASETA,semana_edad_ave,SUM(PORCENTAJE_MORTALIDAD),META_PORCENTAJE_MORTALIDAD 
                               FROM BALANZA_AVES(%s)
                               GROUP BY GRANJA,CASETA,semana_edad_ave,META_PORCENTAJE_MORTALIDAD ORDER BY SEMANA_EDAD_AVE ASC
                           """
                elif self.filtros == 'granja_parvada':
                    query_parvada = """ INSERT INTO bi_crianza_kpi_mortalidad(
                                        granja,
                                        semena_edad_ave,
                                        mortalidad_porcen,
                                        mortalidad_porcen_meta)      
                                        SELECT GRANJA,semana_edad_ave,SUM(PORCENTAJE_MORTALIDAD),META_PORCENTAJE_MORTALIDAD
                                        FROM balanza_aves_parvada(%s,%s)
                                        GROUP BY GRANJA,semana_edad_ave,META_PORCENTAJE_MORTALIDAD ORDER BY SEMANA_EDAD_AVE ASC
                                    """
            elif self.indicador == 'mortalidad_porcentaje_acum':
                if self.filtros == 'granja_caseta':
                    query = """INSERT INTO bi_crianza_kpi_mortalidad(
                               semena_edad_ave,
                               granja,
                               caseta,
                               mortalidad_porcen_acum,
                               mortalidad_porcen_acum_meta)
                               select semana_edad_ave,granja,caseta,SUM(PORCENTAJE_MORTALIDAD_ACUM),SUM(META_MORTALIDAD_ACUM)
                               from balanza_aves(%s)
                               GROUP BY semana_edad_ave,granja,caseta
                               ORDER BY SEMANA_EDAD_AVE ASC
                            """
                elif self.filtros == 'granja_parvada':
                    query_parvada = """INSERT INTO bi_crianza_kpi_mortalidad(
                                        semena_edad_ave,
                                        granja,
                                        mortalidad_porcen_acum,
                                        mortalidad_porcen_acum_meta)
                                        select semana_edad_ave,granja,SUM(PORCENTAJE_MORTALIDAD_ACUM)/7,SUM((META_MORTALIDAD_ACUM)/7)
                                        from balanza_aves_parvada(%s,%s)
                                        GROUP BY semana_edad_ave,granja
                                        ORDER BY SEMANA_EDAD_AVE ASC
                            """
            elif self.indicador == 'consumo_grs_ave':
                if self.filtros == 'granja_caseta':
                    query = """INSERT INTO bi_crianza_kpi_mortalidad(
                                        semena_edad_ave,
                                        granja,
                                        caseta,
                                        consumo_alimento_grs_ave,
                                        consumo_alimento_grs_ave_meta)
                                        select semana_edad_ave,granja,caseta,SUM(consumo_alimento_grs_ave), sum(consumo_alimento_grs_ave_meta)
                                        from balanza_aves(%s)
                                        GROUP BY semana_edad_ave,granja,caseta
                                        order by semana_edad_ave asc
                                         """
                elif self.filtros == 'granja_parvada':
                    query_parvada = """INSERT INTO bi_crianza_kpi_mortalidad(
                                       semena_edad_ave,
                                       granja,
                                       consumo_alimento_grs_ave,
                                       consumo_alimento_grs_ave_meta)
                                       select semana_edad_ave,granja,SUM(consumo_alimento_grs_ave),consumo_alimento_grs_ave_acum_meta
                                       from balanza_aves_parvada(%s,%s)
                                       GROUP BY semana_edad_ave,granja,consumo_alimento_grs_ave_acum_meta
                                       order by semana_edad_ave asc
                                    """
            elif self.indicador == 'consumo_grs_ave_acum':
                if self.filtros == 'granja_caseta':
                    query = """INSERT INTO bi_crianza_kpi_mortalidad(
                                        semena_edad_ave,
                                        granja,
                                        caseta,
                                        consumo_alimento_grs_ave_acum,
                                        consumo_alimento_grs_ave_acum_meta)
                                        select semana_edad_ave,granja,caseta,SUM(consumo_alimento_grs_ave_acum), consumo_alimento_grs_ave_acum_meta
                                        from balanza_aves(%s)
                                        GROUP BY semana_edad_ave,granja,caseta,consumo_alimento_grs_ave_acum_meta
                                        order by semana_edad_ave asc
                                                          """
                elif self.filtros == 'granja_parvada':
                    query_parvada = """INSERT INTO bi_crianza_kpi_mortalidad(
                                       semena_edad_ave,
                                       granja,
                                       consumo_alimento_grs_ave_acum,
                                       consumo_alimento_grs_ave_acum_meta)
                                       select semana_edad_ave,granja,sum(consumo_alimento_grs_ave), (consumo_alimento_grs_ave_acum_meta)
                                       from balanza_aves_parvada(%s,%s)
                                       GROUP BY semana_edad_ave,granja,consumo_alimento_grs_ave_acum_meta
                                       order by semana_edad_ave asc
                                    """
        elif self.periodo == 'dia': ############################## by day
            if self.indicador == 'mortalidad_porcentaje':
                if self.filtros == 'granja_caseta':
                    query = """ INSERT INTO bi_crianza_kpi_mortalidad(
                                             dias_edad_ave,
                                            semena_edad_ave,
                                            granja,
                                            caseta,
                                            mortalidad_porcen,
                                            mortalidad_porcen_meta)
                                            select dias_edad_ave,
                                                   semana_edad_ave,
                                                   granja,
                                                   caseta,
                                                   porcentaje_mortalidad,
                                                   (meta_porcentaje_mortalidad/7) 
                                            from balanza_aves(%s)
                            """
                elif self.filtros == 'granja_parvada':
                    query_parvada = """ INSERT INTO bi_crianza_kpi_mortalidad(
                                                                 dias_edad_ave,
                                                                semena_edad_ave,
                                                                granja,
                                                                mortalidad_porcen,
                                                                mortalidad_porcen_meta)
                                                                  select dias_edad_ave,
                                                                       semana_edad_ave,
                                                                       granja,
                                                                       porcentaje_mortalidad,
                                                                       (meta_porcentaje_mortalidad/7) 
                                                                from balanza_aves_parvada(%s,%s)
                                                """
            elif self.indicador == 'mortalidad_porcentaje_acum':
                if self.filtros == 'granja_caseta':
                    query = """INSERT INTO bi_crianza_kpi_mortalidad(
                               dias_edad_ave,
                               semena_edad_ave,
                               granja,
                               caseta,
                               mortalidad_porcen_acum,
                               mortalidad_porcen_acum_meta)
                               select dias_edad_ave,semana_edad_ave,granja,caseta,PORCENTAJE_MORTALIDAD_ACUM,((META_MORTALIDAD_ACUM)/7)
                               from balanza_aves(%s)
                               """
                elif self.filtros == 'granja_parvada':
                    query_parvada = """INSERT INTO bi_crianza_kpi_mortalidad(
                                                                           dias_edad_ave,
                                                                           semena_edad_ave,
                                                                           granja,
                                                                           mortalidad_porcen_acum,
                                                                           mortalidad_porcen_acum_meta)
                                                                           select dias_edad_ave,semana_edad_ave,granja,caseta,PORCENTAJE_MORTALIDAD_ACUM,((META_MORTALIDAD_ACUM)/7)
                                                                           from balanza_aves_parvada(%s,%s)
                                                                              """
            elif self.indicador == 'consumo_grs_ave':
                if self.filtros == 'granja_caseta':
                    query = """INSERT INTO bi_crianza_kpi_mortalidad(
                                                                      dias_edad_ave,
                                                                      semena_edad_ave,
                                                                      granja,
                                                                      caseta,
                                                                      consumo_alimento_grs_ave,
                                                                      consumo_alimento_grs_ave_meta)
                                                                      select dias_edad_ave,semana_edad_ave,granja,caseta,consumo_alimento_grs_ave, (consumo_alimento_grs_ave_meta)/7
                                                                      from balanza_aves(%s)
                            """
                elif self.filtros == 'granja_parvada':
                    query_parvada = """INSERT INTO bi_crianza_kpi_mortalidad(
                                                                                          dias_edad_ave,
                                                                                          semena_edad_ave,
                                                                                          granja,
                                                                                          consumo_alimento_grs_ave,
                                                                                          consumo_alimento_grs_ave_meta)
                                                                                          select dias_edad_ave,semana_edad_ave,granja,consumo_alimento_grs_ave, (consumo_alimento_grs_ave_meta)
                                                                                          from balanza_aves_parvada(%s,%s)
                                                """
            elif self.indicador == 'consumo_grs_ave_acum':
                if self.filtros == 'granja_caseta':
                    query = """INSERT INTO bi_crianza_kpi_mortalidad(
                                                                    dias_edad_ave,
                                                                    semena_edad_ave,
                                                                    granja,
                                                                    caseta,
                                                                    consumo_alimento_grs_ave_acum,
                                                                    consumo_alimento_grs_ave_acum_meta)
                                                                    select dias_edad_ave,semana_edad_ave,granja,caseta,consumo_alimento_grs_ave_acum, (consumo_alimento_grs_ave_acum_meta)/7
                                                                    from balanza_aves(%s)
                                                """
                elif self.filtros == 'granja_parvada':
                    query_parvada = """INSERT INTO bi_crianza_kpi_mortalidad(
                                                                    dias_edad_ave,
                                                                    semena_edad_ave,
                                                                    granja,
                                                                    consumo_alimento_grs_ave_acum,
                                                                    consumo_alimento_grs_ave_acum_meta)
                                                                    select dias_edad_ave,semana_edad_ave,granja,consumo_alimento_grs_ave_acum, (consumo_alimento_grs_ave_acum_meta)/7
                                                                    from balanza_aves_parvada(%s,%s)
                                                                   """

        if self.filtros == 'granja_caseta':
            params = [self.caseta_id.id]
            self.env.cr.execute(query, tuple(params))
        elif self.filtros == 'granja_parvada':
            params = [self.granja_id.id,self.parvada_id.id]
            self.env.cr.execute(query_parvada, tuple(params))

