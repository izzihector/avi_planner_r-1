-- Function: public.balanza_aves()

-- DROP FUNCTION public.balanza_aves();
-- select dias_edad_ave,semana_edad_ave,granja,caseta,porcentaje_mortalidad,meta_porcentaje_mortalidad from balanza_aves()

CREATE OR REPLACE FUNCTION public.balanza_aves()
  RETURNS TABLE(fecha date, 
		semana_year character varying, 
		semana_edad_ave numeric,
		dias_edad_ave numeric, 
		granja character varying, 
		seccion character varying, 
		caseta character varying, 
		poblacion_inicial numeric, 
		entradas numeric, 
		mortalidad numeric, 
		porcentaje_mortalidad numeric, 
		meta_porcentaje_mortalidad numeric, --meta mortalidad
		mortalidad_acum numeric, 
		porcentaje_mortalidad_acum numeric, 
		poblacion_final numeric) AS
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
  _porcentaje_mortalidad_acum numeric(4,2);
  _poblacion_final numeric;
  _total_recepciones numeric; 
  r record;
  c CURSOR FOR  select date(dd.dd) as Fecha from generate_series ( '2018-11-01'::timestamp , '2018-11-30'::timestamp, '1 day'::interval) dd;
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
				  meta_porcentaje_mortalidad numeric(5,5), --META
				  mortalidad_acum numeric, 
				  porcentaje_mortalidad_acum numeric(4,2), 
				  poblacion_final  numeric);
  FOR r IN c LOOP
	--parvada TODO: Falta asignardlo como parametro
	_parvada_id = 1;
	-- Para obtener la edad de la parvada
	_fecha_primer_recepcion := (select fecha_recepcion from bi_parvada_recepcion bpr where parvada_id = 1 and bpr.caseta_id = 1 order by fecha_recepcion asc limit 1);
	_fecha_ultima_recepcion := (select fecha_recepcion from bi_parvada_recepcion bpr where parvada_id = 1 and bpr.caseta_id = 1 order by fecha_recepcion desc limit 1);	
        _dias_diff_fechas := (date_part('day',age(_fecha_ultima_recepcion, _fecha_primer_recepcion)))/2;
        _fecha_inicial_edad_ave := _fecha_primer_recepcion + interval '1 days';
        _dias_edad_ave := (select date_part('day', age(r.fecha,_fecha_inicial_edad_ave)));
        _semana_edad_ave:= (select date_part('day', age(r.fecha,_fecha_inicial_edad_ave))/7);
        
	--granja
    _granja := (select ga.name from bi_granja_caseta ca inner join bi_granja ga on ga.id = ca.granja_id where ca.id = 1);	 
	--seccion
    _seccion := (select s.name from bi_granja_caseta ca inner join bi_granja_seccion s on s.id = ca.seccion_id where ca.id =1);  
	--caseta
    _caseta := (select ca.name from bi_granja_caseta ca where ca.id = 1);  
	--poblacion inicial
	_poblacion_inicial := (select BA.poblacion_final from BALANZA_AVES BA where BA.fecha = (r.fecha - interval '1 day'));
	--entradas
	_entradas:= (select COALESCE(sum(bpr.poblacion_entrante),0) from bi_parvada_recepcion bpr where bpr.fecha_recepcion = r.fecha and bpr.caseta_id =1 and bpr.parvada_id = 1); 
	--mortalidad
	_mortalidad := (select COALESCE(sum(causa_seleccion),0) + COALESCE(sum(causa_paralitica),0) + COALESCE(sum(causa_natural),0) + COALESCE(sum(causa_sacrificada),0) from bi_parvada_mortalidad bpm where bpm.fecha = r.fecha and  bpm.caseta_id = 1 and bpm.parvada_id = 1);
	--porcentaje de mortalidad
	_porcentaje_mortalidad := CASE WHEN _poblacion_inicial = 0 then 0.00000 ELSE COALESCE(_mortalidad,0) / COALESCE(_poblacion_inicial,1)*100 END;
	_meta_porcentaje_mortalidad := (select crianza_meta_mortalidad from bi_parametros where crianza_edad_semana = round(_semana_edad_ave,0));
	--mortalidad acumulado
	_mortalidad_acum := COALESCE((select BA.mortalidad_acum from BALANZA_AVES BA where BA.fecha = (r.fecha - interval '1 day')),0) + _mortalidad;			    
	--poblacion final
	
    _poblacion_final := COALESCE(_poblacion_inicial,0) + COALESCE(_entradas,0) - COALESCE(_mortalidad,0); 
	--semana del año
    _semana_year := (SELECT date_part('week',r.fecha));
	--total de recepciones en la caseta
     _total_recepciones:= (select COALESCE(sum(bpr.poblacion_entrante),0) from bi_parvada_recepcion bpr where bpr.caseta_id = 3); 
     --porcentaje de mortalidad acumulado
     _porcentaje_mortalidad_acum := CASE WHEN _total_recepciones = 0 then 0.00000 ELSE COALESCE(_mortalidad_acum,0) / COALESCE(_total_recepciones,1)*100 END;
        
        
        RAISE NOTICE 'semana edad del ave %',_semana_edad_ave;
	INSERT INTO BALANZA_AVES VALUES(r.fecha,
					_semana_year,
					_semana_edad_ave,
					_dias_edad_ave,_granja,
					_seccion,_caseta,
					_poblacion_inicial,
					_entradas,
					_mortalidad,
					_porcentaje_mortalidad,
					_meta_porcentaje_mortalidad,
					_mortalidad_acum,
					_porcentaje_mortalidad_acum,
					_poblacion_final);
  END LOOP;  

  RETURN QUERY SELECT * FROM BALANZA_AVES;
  
END;
$BODY$
  LANGUAGE plpgsql VOLATILE
