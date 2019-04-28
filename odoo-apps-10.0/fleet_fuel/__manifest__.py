# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.

{
    'name': 'Limited Fuel - Fleet Management',
    'author': 'Makepler Sistemas',
    'company': 'Makepler Sistemas',
    'version': '10.0.0.1.0',
    'license': 'AGPL-3',
    'website': 'https://www.makepler.com',
    'category': 'Managing limited fuel per period',
    'description': """
        This module extends the fleet module and provides extra features and
        manage fleet fuel.
    """,
    'summary': """
        fleet management
        fleet fuel
    """,
    'depends': ['fleet'],
    'data': [
              'views/fleet_extended_view.xml',
              ],
    'installable': True,
    'application': True,
    'images': ['static/description/background-fuel.png'],
}
