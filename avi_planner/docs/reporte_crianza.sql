	select
			date(dd.dd),
			ga.name granja, 
			s.name seccion,
			ca.name caseta, 
			LAG ((sum(d.t_poblacion_traspaso) - 
				  (sum(mo.muertes_seleccion) + 
				   sum(mo.muertes_paraliticas) +  
				   sum(mo.muertes_naturales) ))) 
				   OVER (ORDER BY dd.dd) as poblacion_inicial ,
		   CASE 
		      WHEN (sum(d.t_poblacion_traspaso) is null) THEN 0
			  ELSE sum(d.t_poblacion_traspaso)
		   END Entradas,
		   CASE
		   		WHEN ((sum(mo.muertes_seleccion) +  sum(mo.muertes_paraliticas) +  sum(mo.muertes_naturales)) is null) THEN 0
				ELSE sum(mo.muertes_seleccion) +  sum(mo.muertes_paraliticas) +  sum(mo.muertes_naturales)
		   END Salidas,
		   CASE
		   		WHEN ((sum(d.t_poblacion_traspaso) -  (sum(mo.muertes_seleccion) + sum(mo.muertes_paraliticas) +  sum(mo.muertes_naturales))) is null) THEN 0
		   		ELSE sum(d.t_poblacion_traspaso) - (sum(mo.muertes_seleccion) + sum(mo.muertes_paraliticas) +   sum(mo.muertes_naturales))
		   END poblacion_final
	from bi_granja_seccion_caseta rel_g
	right join bi_granja ga on ga.id = rel_g.granja_id
	right join bi_granja_seccion s on s.id = rel_g.seccion_id
	right join bi_granja_caseta ca on ca.id = rel_g.caseta_id
	inner join bi_parvada_distribucion d on d.granja_seccion_caseta_destino_rel_id = rel_g.id
	inner join bi_parvada_mortalidad mo on mo.granja_seccion_caseta_origen_rel_id = rel_g.id
	right join generate_series ( '2018-01-01'::timestamp , '2018-12-31'::timestamp, '1 day'::interval) dd 
								on d.fecha_traspaso = dd.dd  or mo.fecha_mortalidad = dd.dd
	group by dd.dd,mo.fecha_mortalidad,d.fecha_traspaso,ga.name,s.name,ca.name
	order by dd.dd asc

