# -*- coding: utf-8 -*-
#This file is part of Tryton.  The COPYRIGHT file at the top level of
#this repository contains the full copyright notices and license terms.
{
    'name' : 'Party - vCardDAV',
    'name_de_DE': 'Parteien vCardDAV',
    'name_es_CO' : 'vCardDAV de Compañía',
    'version' : '0.0.1',
    'author' : 'B2CK',
    'email': 'info@b2ck.com',
    'website': 'http://www.tryton.org/',
    'description': 'Add CardDAV on parties',
    'description_de_DE': 'Ermöglicht CardDAV für Parteien',
    'description_es_CO': 'Soporte de CardDAV para terceros',
    'depends' : [
        'ir',
        'res',
        'party',
        'webdav',
    ],
    'xml' : [
        'party.xml',
    ],
    'translation': [
        'de_DE.csv',
        'es_CO.csv',
    ],
}
