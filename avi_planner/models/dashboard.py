from odoo import fields, models, api


class AviplannerDashboard(models.Model):
    _name = "avi.dashboard"

    name = fields.Char(string="")
    granja = fields.Char(string="")

    @api.model
    def get_granjas(self):
        granja = self.env['bi.granja'].sudo().search_read([])
        return granja

    @api.model
    def get_parvadas(self):
        parvada = self.env['bi.parvada'].sudo().search_read([])
        return parvada

    @api.model
    def get_granjas_info(self, parameters):
        # aves)
        granja = self.env['bi.granja'].sudo().search_read([])
        # aves recibidas
        recepciones_objs = self.env['bi.parvada.recepcion'].search(
            [('granja_id', '=', int(parameters['parameters']['granja_id'])),
             ('parvada_id', '=', int(parameters['parameters']['parvada_id']))])
        suma_recepciones = 0
        if recepciones_objs is not None:
            for e in recepciones_objs:
                suma_recepciones += e.poblacion_entrante

        envios_objs = self.env['bi.parvada.distribucion'].search(
            [('granja_id', '=', int(parameters['parameters']['granja_id'])),
             ('parvada_id', '=', int(parameters['parameters']['parvada_id'])),
             ('causa_traspaso_id', '=', 3)])

        suma_envios_postura = 0
        if envios_objs is not None:
            for eo in envios_objs:
                suma_envios_postura += eo.t_poblacion_traspaso
        suma_mortalidad = 0
        mortalidad_objs = self.env['bi.parvada.mortalidad'].search(
            [('granja_id', '=', int(parameters['parameters']['granja_id'])),
             ('parvada_id', '=', int(parameters['parameters']['parvada_id']))])
        if mortalidad_objs is not None:
            for m in mortalidad_objs:
                suma_mortalidad += m.total_mortalidad

        alimento_entrada_objs = self.env['bi.registro.alimento'].search(
            [('granja_id', '=', int(parameters['parameters']['granja_id'])),
             ('parvada_id', '=', int(parameters['parameters']['parvada_id']))])
        suma_alimento_entrada = 0
        suma_alimento_consumo = 0.0
        if alimento_entrada_objs is not None:
            for a in alimento_entrada_objs:
                suma_alimento_entrada += a.kgs_entrada
                suma_alimento_consumo += a.consumo

        self.env['bi.kpis'].search([]).unlink()
        self._sql_report_object_informe()
        self._sql_mortalidad_acum(parameters)

        granja_name = self.env['bi.granja'].search([('id', '=', int(parameters['parameters']['granja_id']))])
        mortalidad_acum_objs = self.env['bi.kpis'].search(
            [('granja', '=', granja_name.name), ('semena_edad_ave', '=', 18)])

        mortalidad_acum_info = self.env['bi.kpis'].sudo().search_read([])

        self.env['bi.kpis'].search([]).unlink()
        self._sql_report_object_informe()
        self._sql_mortalidad(parameters)

        mortalidad_info = self.env['bi.kpis'].sudo().search_read([])

        self.env['bi.kpis'].search([]).unlink()
        self._sql_report_object_informe()
        self._sql_consumo_grs_acumulados(parameters)

        consumo_grs_acum_info = self.env['bi.kpis'].sudo().search_read([])

        self.env['bi.kpis'].search([]).unlink()
        self._sql_report_object_informe()
        self._sql_consumo_grs(parameters)

        consumo_grs_info = self.env['bi.kpis'].sudo().search_read([])

        self.env['bi.kpis'].search([]).unlink()
        self._sql_report_object_informe()
        self._sql_peso(parameters)

        peso_info = self.env['bi.kpis'].sudo().search_read([])

        self.env['bi.kpis'].search([]).unlink()
        self._sql_report_object_informe()
        self._sql_uniformidad(parameters)

        uniformidad_info = self.env['bi.kpis'].sudo().search_read([])

        mortalidad_porcen_cierre = 0
        if suma_recepciones > 0 and suma_envios_postura > 0:
            mortalidad_porcen_cierre = (float(
                suma_mortalidad + (suma_recepciones - suma_envios_postura - suma_mortalidad)) / float(
                suma_recepciones)) * 100
        grs_acum_consum_enviados = 0
        if suma_alimento_entrada > 0:
            grs_acum_consum_enviados = round((float((float(suma_alimento_entrada) / float(suma_recepciones)) * 1000)),
                                             2)
        grs_acum_consum_servido = 0
        if suma_alimento_consumo > 0:
            grs_acum_consum_servido = round((float((float(suma_alimento_entrada) / float(suma_recepciones)) * 1000)),
                                            2)

        if granja:
            data = {
                'ave_recibida': suma_recepciones,
                'ave_enviada': suma_envios_postura,
                'mortalidad_total': suma_mortalidad,
                'diff_aves': suma_recepciones - suma_envios_postura - suma_mortalidad,
                'mortalidad_al_cierre': round(mortalidad_porcen_cierre, 2),
                'alimento_enviado': suma_alimento_entrada,
                'alimento_consumido': suma_alimento_consumo,
                'grs_acum_consum_enviados': grs_acum_consum_enviados,
                'grs_acum_consum_servido': grs_acum_consum_servido,
                'mortalidad_acum_info': mortalidad_acum_info,
                'mortalidad_info': mortalidad_info,
                'consumo_acum_info': consumo_grs_acum_info,
                'consumo_info': consumo_grs_info,
                'peso_info': peso_info,
                'uniformidad_info':uniformidad_info,
            }
        granja[0].update(data)
        return granja

    def _sql_report_object_informe(self):
        query_funcion_parvada = """
            CREATE OR REPLACE FUNCTION public.balanza_aves_parvada(
            IN x_granja_id integer,
            IN x_parvada_id integer)
          RETURNS TABLE(fecha date, semana_year character varying, semana_edad_ave numeric, dias_edad_ave numeric, granja character varying, poblacion_inicial numeric, entradas numeric, mortalidad numeric, porcentaje_mortalidad numeric, meta_porcentaje_mortalidad numeric, mortalidad_acum numeric, porcentaje_mortalidad_acum numeric, meta_mortalidad_acum numeric, poblacion_final numeric, consumo_alimento_kgs_total numeric, consumo_alimento_grs_ave numeric, consumo_alimento_grs_ave_meta numeric, consumo_alimento_grs_ave_acum numeric, consumo_alimento_grs_ave_acum_meta numeric, peso_real numeric, peso_meta numeric, uniformidad_real numeric, uniformidad_meta numeric) AS
        $BODY$
                DECLARE
                  _parvada_id numeric;
                  _fecha_nacimiento date;
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
                  _porcentaje_mortalidad numeric;
                  _meta_porcentaje_mortalidad numeric; --- META
                  _mortalidad_acum numeric;
                  _meta_mortalidad_acum numeric;
                  _porcentaje_mortalidad_acum numeric;
                  _poblacion_final numeric;
                  _total_recepciones numeric; 
                  _fecha_inicio_cursor date;
                  _fecha_finaliza_curos date;

                  r record;
                  c CURSOR FOR  select date(dd.dd) as Fecha from
        generate_series (_fecha_inicio_cursor ::timestamp,(_fecha_inicio_cursor + interval '132 day')::timestamp, '1 day'::interval) dd;
        _consumo_alimento_kgs_total numeric;
        _consumo_alimento_grs_ave numeric;
        _consumo_alimento_grs_ave_meta numeric;
        _consumo_alimento_grs_ave_acum numeric;
        _consumo_alimento_grs_ave_acum_meta numeric;
        _peso_meta numeric;
        _peso_real numeric;
        _uniformidad_meta numeric;
        _uniformidad_real numeric;
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
                                  porcentaje_mortalidad numeric,
                                  meta_porcentaje_mortalidad numeric,
                                  mortalidad_acum numeric, 
                                  meta_mortalidad_acum numeric,
                                  porcentaje_mortalidad_acum numeric, 
                                  poblacion_final  numeric,
                                  consumo_alimento_kgs_total numeric,
                                  consumo_alimento_grs_ave numeric,
                                  consumo_alimento_grs_ave_meta numeric,
                                  consumo_alimento_grs_ave_acum numeric,
                                  consumo_alimento_grs_ave_acum_meta numeric,
                                  peso_real numeric,peso_meta numeric,                          
                                  uniformidad_real numeric,uniformidad_meta numeric);


        	  _fecha_inicio_cursor := (select fecha_nacimiento from bi_parvada  bpr where id = x_parvada_id limit 1);
        	  IF _fecha_inicio_cursor  is not null
        	  THEN
        		  FOR r IN c LOOP
        		    -- Para obtener la edad de la parvada
        		    _fecha_nacimiento :=(select fecha_nacimiento from bi_parvada  bpr where id = x_parvada_id limit 1);
        		    _fecha_inicial_edad_ave := _fecha_nacimiento + interval '1 days';
        		    _dias_edad_ave := (select r.fecha::date - _fecha_nacimiento::date);
        		    RAISE NOTICE 'Fecha actual  % y fecha recepcion % y dia %',r.fecha,_fecha_nacimiento,(select date_part('day', age(r.fecha, _fecha_nacimiento)));
        		    _semana_edad_ave:= ((select r.fecha::date  -  _fecha_nacimiento::date)/7);
        		    --granja
        		    _granja := (select ga.name from bi_granja ga where ga.id = x_granja_id);	 
        		    --poblacion inicial
        		    _poblacion_inicial := (select BA.poblacion_final from BALANZA_AVES BA where BA.fecha = (r.fecha - interval '1 day'));
        		    --entradas
        		    _entradas:= (select COALESCE(sum(bpr.poblacion_entrante),0) from bi_parvada_recepcion bpr where bpr.fecha_nacimiento = r.fecha and bpr.parvada_id = x_parvada_id and bpr.granja_id = x_granja_id); 
        		    --mortalidad
        		    _mortalidad := (select COALESCE(sum(causa_seleccion),0) + COALESCE(sum(causa_paralitica),0) + COALESCE(sum(causa_natural),0) + COALESCE(sum(causa_sacrificada),0) from bi_parvada_mortalidad bpm where bpm.fecha = r.fecha and bpm.parvada_id = x_parvada_id 
        				    and bpm.granja_id = x_granja_id);
        		    --porcentaje de mortalidad
        		     _porcentaje_mortalidad := CASE WHEN COALESCE(_poblacion_inicial,0) = 0 then 0.00000 ELSE COALESCE(_mortalidad,0) /  COALESCE(_poblacion_inicial,1)*100 END;
        		    _meta_porcentaje_mortalidad := (select crianza_meta_mortalidad from bi_parametros where crianza_edad_semana = round(_semana_edad_ave,0));
        		    --mortalidad acumulado
        		    _mortalidad_acum := COALESCE((select BA.mortalidad_acum from BALANZA_AVES BA where BA.fecha = (r.fecha - interval '1 day')),0) + _mortalidad;            			    
        		    _meta_mortalidad_acum := (select crianza_meta_mortalidad_acum from bi_parametros where crianza_edad_semana = round(_semana_edad_ave,0));
        		    --poblacion final
        		    _poblacion_final := COALESCE(_poblacion_inicial,0) + COALESCE(_entradas,0) - COALESCE(_mortalidad,0); 
        		    _semana_year := (SELECT date_part('week',r.fecha));
        		    --total de recepciones en la caseta
        		    _total_recepciones:= (select COALESCE(sum(bpr.poblacion_entrante),0) from bi_parvada_recepcion bpr where bpr.parvada_id = x_parvada_id and bpr.granja_id = x_granja_id); 
        		     --porcentaje de mortalidad acumulado
        		    _porcentaje_mortalidad_acum := CASE WHEN _total_recepciones = 0 then 0.00000 ELSE COALESCE(_mortalidad_acum,0) / COALESCE(_total_recepciones,1)*100 END;

        		    _consumo_alimento_kgs_total := (SELECT COALESCE(sum(consumo),0) FROM public.bi_registro_alimento bra 
        					  where bra.fecha = r.fecha and bra.tipo_evento_id = 2 and bra.state= 'finished' and bra.parvada_id = x_parvada_id and bra.parvada_id = x_granja_id) ;

        		    _consumo_alimento_grs_ave := CASE WHEN _consumo_alimento_kgs_total = 0 then 0 ELSE ((_consumo_alimento_kgs_total  * 1000) / _poblacion_inicial) END;
        		    _consumo_alimento_grs_ave_meta := (select crianza_meta_cons_alim_grs from bi_parametros where crianza_edad_semana = round(_semana_edad_ave,0));
        		    _consumo_alimento_grs_ave_acum := COALESCE((select BA.consumo_alimento_grs_ave_acum from BALANZA_AVES BA where BA.fecha = (r.fecha - interval '1 day')),0) + _consumo_alimento_grs_ave;
        		    _consumo_alimento_grs_ave_acum_meta := (select crianza_meta_cons_alim_acum_grs from bi_parametros where crianza_edad_semana = round(_semana_edad_ave,0));


                            _peso_real := (SELECT sum(pu.peso)/count(pu.peso) FROM public.bi_peso_uniformidad pu where pu.fecha = r.fecha and pu.parvada_id = x_parvada_id and pu.granja_id = x_granja_id);
        		    _peso_meta := (select crianza_meta_peso_corporal from  bi_parametros where crianza_edad_semana = round(_semana_edad_ave,0));
        		    _uniformidad_real := (SELECT sum(pu.uniformidad)/count(pu.uniformidad)FROM public.bi_peso_uniformidad pu where pu.fecha = r.fecha and pu.parvada_id = x_parvada_id and pu.granja_id = x_granja_id);
                            _uniformidad_meta := (select crianza_meta_uniformidad from  bi_parametros where crianza_edad_semana = round(_semana_edad_ave,0));

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
        				    _consumo_alimento_grs_ave_acum_meta,
        				    _peso_real,
        				    _peso_meta,
        				    _uniformidad_real,
        				    _uniformidad_meta);
        		  END LOOP;  
        	  END IF;
                  RETURN QUERY SELECT * FROM BALANZA_AVES;

                END;
                $BODY$
          LANGUAGE plpgsql VOLATILE

                    """
        self.env.cr.execute(query_funcion_parvada)

    def _sql_mortalidad_acum(self, parameters):
        query_parvada = """INSERT INTO  bi_kpis(
                                              semena_edad_ave,
                                              granja,
                                              mortalidad_porcen_acum,
                                              mortalidad_porcen_acum_meta)
                                              select semana_edad_ave,granja,SUM(PORCENTAJE_MORTALIDAD_ACUM)/7,SUM((META_MORTALIDAD_ACUM)/7)
                                              from balanza_aves_parvada(%s,%s)
                                              GROUP BY semana_edad_ave,granja
                                              ORDER BY SEMANA_EDAD_AVE ASC
                                  """
        params = [int(parameters['parameters']['granja_id']), int(parameters['parameters']['parvada_id'])]
        self.env.cr.execute(query_parvada, tuple(params))

    def _sql_mortalidad(self, parameters):
        query_parvada = """ INSERT INTO  bi_kpis(
                                                granja,
                                                semena_edad_ave,
                                                mortalidad_porcen,
                                                mortalidad_porcen_meta)      
                                                SELECT GRANJA,semana_edad_ave,SUM(PORCENTAJE_MORTALIDAD),META_PORCENTAJE_MORTALIDAD
                                                FROM balanza_aves_parvada(%s,%s)
                                                GROUP BY GRANJA,semana_edad_ave,META_PORCENTAJE_MORTALIDAD ORDER BY SEMANA_EDAD_AVE ASC
                                            """

        params = [int(parameters['parameters']['granja_id']), int(parameters['parameters']['parvada_id'])]
        self.env.cr.execute(query_parvada, tuple(params))

    def _sql_consumo_grs_acumulados(self, parameters):
        query_parvada = """INSERT INTO bi_kpis(
                                          semena_edad_ave,
                                          granja,
                                          consumo_alimento_grs_ave_acum,
                                          consumo_alimento_grs_ave_acum_meta)
                                          select semana_edad_ave,granja,sum(consumo_alimento_grs_ave_acum)/7,consumo_alimento_grs_ave_acum_meta
                                          from balanza_aves_parvada(%s,%s)
                                          GROUP BY semana_edad_ave,granja,consumo_alimento_grs_ave_acum_meta
                                          order by semana_edad_ave asc

                                       """

        params = [int(parameters['parameters']['granja_id']), int(parameters['parameters']['parvada_id'])]
        self.env.cr.execute(query_parvada, tuple(params))

    def _sql_consumo_grs(self, parameters):
        query_parvada = """INSERT INTO  bi_kpis(
                                               semena_edad_ave,
                                               granja,
                                               consumo_alimento_grs_ave,
                                               consumo_alimento_grs_ave_meta)
                                               select semana_edad_ave,granja,SUM(consumo_alimento_grs_ave),SUM(consumo_alimento_grs_ave_meta)
                                               from balanza_aves_parvada(%s,%s)
                                               GROUP BY semana_edad_ave,granja
                                               order by semana_edad_ave asc
                                            """

        params = [int(parameters['parameters']['granja_id']), int(parameters['parameters']['parvada_id'])]
        self.env.cr.execute(query_parvada, tuple(params))

    def _sql_peso(self, parameters):
        query_parvada = """INSERT INTO  bi_kpis(
                                                                 semena_edad_ave,
                                                                 granja,
                                                                 peso_real,
                                                                 peso_meta)
                                                                 SELECT semana_edad_ave,GRANJA,CASE WHEN (COUNT(PESO_REAL) = 0) THEN sum(COALESCE(PESO_REAL,0)) ELSE sum(COALESCE(PESO_REAL,0))/COUNT(PESO_REAL) END  PESO_REAL,PESO_META
                                                                 FROM balanza_aves_parvada(%s,%s)
                                                                 GROUP BY GRANJA,semana_edad_ave,PESO_META ORDER BY SEMANA_EDAD_AVE ASC
                                               """
        params = [int(parameters['parameters']['granja_id']), int(parameters['parameters']['parvada_id'])]
        self.env.cr.execute(query_parvada, tuple(params))

    def _sql_uniformidad(self, parameters):
        query_parvada = """INSERT INTO  bi_kpis(
                                                              semena_edad_ave,
                                                              granja,
                                                              uniformidad_real,
                                                              uniformidad_meta)
                                                              SELECT semana_edad_ave,GRANJA,CASE WHEN (COUNT(uniformidad_real) = 0) THEN sum(COALESCE(uniformidad_real,0)) ELSE sum(COALESCE(uniformidad_real,0))/COUNT(uniformidad_real) END  uniformidad_real,uniformidad_meta
                                                              FROM balanza_aves_parvada(%s,%s)
                                                              GROUP BY GRANJA,semana_edad_ave,uniformidad_meta ORDER BY SEMANA_EDAD_AVE ASC

                                                           """
        params = [int(parameters['parameters']['granja_id']), int(parameters['parameters']['parvada_id'])]
        self.env.cr.execute(query_parvada, tuple(params))
