# -*- coding: utf-8 -*-
{
    'name' : 'AVI Planner',
    'category': 'Inventory',
    'sequence': 1000,
    'summary': 'Administracion de granjas de Crianza y Postura',
    'description' : """
        Parvadas, Aves, Mortalidad, Empaque, Alimento
        """,
    'author':'Ivan Porras',
    'website': 'www.makepler.com',
    'version': '10.0.0.0',
    "support": "ivan.porras@makepler.com",
    "price": 499.00,
    "currency": "EUR",
    # any module necessary for this one to work correctly
    'depends': ['web_readonly_bypass','web_widget_bokeh_chart','base','mail'],

    'data': [
        'views/bi_view_tree.xml',        
        'views/bi_view_form.xml',        
        'views/bi_view_graph.xml',
        'views/bi_view.xml',
        'wizard/bi_view_report_kpi.xml',
        'wizard/bi_view_report_kpi_postura.xml',
        'wizard/bi_resumen_parvada.xml',
        'data/data_avi_planner.xml'        
    ],

    'installable': True,
    'application': True,
}
