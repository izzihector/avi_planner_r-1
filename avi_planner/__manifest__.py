# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name' : 'AVI Planner',
    'version' : '1.0.0',
    'category': 'Inventory',
    'author':'Ivan Porras',
    'website' : 'www.makepler.com',
    'summary' : 'AVI Planner',
    'description' : """
Parvadas, Aves, Mortalidad, Empaque, Alimento
==================================
""",
    "author": "Makepler Sistemas",
    "website": "https://makepler.com/",
    "support": "ivan.porras@makepler.com",
    "price": 499.00,
    "currency": "EUR",
    
    'depends': ['web_readonly_bypass','web_widget_bokeh_chart','base','mail'],
    'data': [
        'views/bi_view_tree.xml',        
        'views/bi_view_form.xml',        
        'views/bi_view_graph.xml',
        'views/bi_view.xml',
        'wizard/bi_view_report_kpi.xml',
        'data/data_avi_planner.xml'        
    ],

    'installable': True,
    'application': True,
}
