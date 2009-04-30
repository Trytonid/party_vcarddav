#This file is part of Tryton.  The COPYRIGHT file at the top level of
#this repository contains the full copyright notices and license terms.

from DAV import propfind
from trytond.protocols.webdav import TrytonDAVInterface

_mk_prop_response = propfind.PROPFIND.mk_prop_response

def mk_prop_response(self, uri, good_props, bad_props, doc):
    res = _mk_prop_response(self, uri, good_props, bad_props, doc)
    dbname, uri = TrytonDAVInterface.get_dburi(uri)
    if uri in ('Contacts', 'Contacts/'):
        #ad = doc.createElement('addressbook')
        #ad.setAttribute('xmlns', 'urn:ietf:params:xml:ns:carddav')
        vc = doc.createElement('vcard-collection')
        vc.setAttribute('xmlns', 'http://groupdav.org/')
        cols = res.getElementsByTagName('D:collection')
        if cols:
            #cols[0].parentNode.appendChild(ad)
            cols[0].parentNode.appendChild(vc)
    return res

propfind.PROPFIND.mk_prop_response = mk_prop_response
