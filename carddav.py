#This file is part of Tryton.  The COPYRIGHT file at the top level of
#this repository contains the full copyright notices and license terms.

from DAV import propfind
from DAV.errors import *
from trytond.protocols.webdav import TrytonDAVInterface, USER_ID, CACHE, DATABASE
from trytond.pool import Pool

TrytonDAVInterface.PROPS['urn:ietf:params:xml:ns:carddav'] = (
        'address-data',
        'addressbook-data',
    )
TrytonDAVInterface.M_NS['urn:ietf:params:xml:ns:carddav'] = '_get_carddav'

propfind.PROPFIND._mk_prop_response = propfind.PROPFIND.mk_prop_response

def mk_prop_response(self, uri, good_props, bad_props, doc):
    res = propfind.PROPFIND._mk_prop_response(self, uri, good_props, bad_props, doc)
    dbname, uri = TrytonDAVInterface.get_dburi(uri)
    if uri in ('Contacts', 'Contacts/'):
        ad = doc.createElement('addressbook')
        ad.setAttribute('xmlns', 'urn:ietf:params:xml:ns:carddav')
        vc = doc.createElement('vcard-collection')
        vc.setAttribute('xmlns', 'http://groupdav.org/')
        cols = res.getElementsByTagName('D:collection')
        if cols:
            cols[0].parentNode.appendChild(ad)
            cols[0].parentNode.appendChild(vc)
    return res

propfind.PROPFIND.mk_prop_response = propfind.PROPFIND.mk_prop_response

def _get_carddav_address_data(self, uri):
    dbname, dburi = self._get_dburi(uri)
    cursor = DATABASE['cursor']
    pool = Pool(DATABASE['dbname'])
    collection_obj = pool.get('webdav.collection')
    try:
        res = collection_obj.get_address_data(cursor, int(USER_ID), dburi,
                cache=CACHE)
    except (DAV_Error, DAV_NotFound, DAV_Secret, DAV_Forbidden):
        raise
    except:
        raise DAV_Error(500)
    return res

TrytonDAVInterface._get_carddav_address_data = _get_carddav_address_data
TrytonDAVInterface._get_carddav_addressbook_data = _get_carddav_address_data
