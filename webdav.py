#This file is part of Tryton.  The COPYRIGHT file at the top level of
#this repository contains the full copyright notices and license terms.
from trytond.model import ModelView, ModelSQL
from DAV.errors import DAV_NotFound, DAV_Forbidden
import base64


class Collection(ModelSQL, ModelView):

    _name = "webdav.collection"

    def vcard(self, cursor, user, uri, context=None):
        '''
        Return party ids of the vcard in uri or False

        :param cursor: the database cursor
        :param user: the user id
        :param uri: the uri
        :param context: the context
        :return: party id
            or None if there is no party
            or False if not in Contacts
        '''
        party_obj = self.pool.get('party.party')

        if uri.startswith('Contacts/'):
            uuid = uri[9:-4]
            party_ids = party_obj.search(cursor, user, [
                ('uuid', '=', uuid),
                ], limit=1, context=context)
            if party_ids:
                return party_ids[0]
            return None
        return False

    def get_childs(self, cursor, user, uri, context=None, cache=None):
        party_obj = self.pool.get('party.party')

        if uri in ('Contacts', 'Contacts/'):
            party_ids = party_obj.search(cursor, user, [], context=context)
            parties = party_obj.browse(cursor, user, party_ids, context=context)
            return [x.uuid + '.vcf' for x in parties]
        party_id = self.vcard(cursor, user, uri, context=context)
        if party_id or party_id is None:
            return []
        res = super(Collection, self).get_childs(cursor, user, uri,
                context=context, cache=cache)
        if not uri:
            res.append('Contacts')
        return res

    def get_resourcetype(self, cursor, user, uri, context=None, cache=None):
        from DAV.constants import OBJECT
        if self.vcard(cursor, user, uri, context=context):
            return OBJECT
        return super(Collection, self).get_resourcetype(cursor, user, uri,
                context=context, cache=cache)

    def get_contenttype(self, cursor, user, uri, context=None, cache=None):
        if self.vcard(cursor, user, uri, context=context):
            return 'text/x-vcard'
        return super(Collection, self).get_contenttype(cursor, user, uri,
                context=context, cache=cache)

    def get_creationdate(self, cursor, user, uri, context=None, cache=None):
        party_obj = self.pool.get('party.party')
        party_id = self.vcard(cursor, user, uri, context=context)
        if party_id is None:
            raise DAV_NotFound
        if party_id:
            cursor.execute('SELECT EXTRACT(epoch FROM create_date) ' \
                    'FROM "' + party_obj._table + '" ' \
                        'WHERE id = %s', (party_id,))
            if cursor.rowcount:
                return cursor.fetchone()[0]
        return super(Collection, self).get_creationdate(cursor, user, uri,
                context=context, cache=cache)

    def get_lastmodified(self, cursor, user, uri, context=None, cache=None):
        party_obj = self.pool.get('party.party')
        address_obj = self.pool.get('party.address')
        contact_mechanism_obj = self.pool.get('party.contact_mechanism')

        party_id = self.vcard(cursor, user, uri, context=context)
        if party_id is None:
            raise DAV_NotFound
        if party_id:
            cursor.execute('SELECT ' \
                    'MAX(EXTRACT(epoch FROM COALESCE(p.write_date, p.create_date))), ' \
                    'MAX(EXTRACT(epoch FROM COALESCE(a.write_date, a.create_date))), ' \
                    'MAX(EXTRACT(epoch FROM COALESCE(c.write_date, c.create_date))) ' \
                    'FROM "' + party_obj._table + '" p ' \
                        'LEFT JOIN "' + address_obj._table + '" a ' \
                        'ON p.id = a.party ' \
                        'LEFT JOIN "' + contact_mechanism_obj._table + '" c ' \
                        'ON p.id = c.party ' \
                    'WHERE p.id = %s', (party_id,))
            return max(cursor.fetchone())
        return super(Collection, self).get_lastmodified(cursor, user, uri,
                context=context, cache=cache)

    def get_data(self, cursor, user, uri, context=None, cache=None):
        vcard_obj = self.pool.get('party_vcarddav.party.vcard', type='report')
        party_id = self.vcard(cursor, user, uri, context=context)
        if party_id is None:
            raise DAV_NotFound
        if party_id:
            val = vcard_obj.execute(cursor, user, [party_id],
                    {'id': party_id, 'ids': [party_id]},
                    context=context)
            return base64.decodestring(val[1])
        return super(Collection, self).get_data(cursor, user, uri,
                context=context, cache=cache)

    def put(self, cursor, user, uri, data, content_type, context=None,
            cache=None):
        party_id = self.vcard(cursor, user, uri, context=context)
        if party_id is None:
            raise DAV_Forbidden
        if party_id:
            raise DAV_Forbidden
        return super(Collection, self).put(cursor, user, uri, data,
                content_type, context=context)

    def mkcol(self, cursor, user, uri, context=None, cache=None):
        party_id = self.vcard(cursor, user, uri, context=context)
        if party_id is None:
            raise DAV_Forbidden
        if party_id:
            raise DAV_Forbidden
        return super(Collection, self).mkcol(cursor, user, uri, context=context,
                cache=cache)

    def rmcol(self, cursor, user, uri, context=None, cache=None):
        party_id = self.vcard(cursor, user, uri, context=context)
        if party_id is None:
            raise DAV_Forbidden
        if party_id:
            raise DAV_Forbidden
        return super(Collection, self).rmcol(cursor, user, uri, context=context,
                cache=cache)

    def rm(self, cursor, user, uri, context=None, cache=None):
        party_id = self.vcard(cursor, user, uri, context=context)
        if party_id is None:
            raise DAV_Forbidden
        if party_id:
            raise DAV_Forbidden
        return super(Collection, self).rm(cursor, user, uri, context=context,
                cache=cache)

    def exists(self, cursor, user, uri, context=None, cache=None):
        party_id = self.vcard(cursor, user, uri, context=context)
        if party_id is None:
            return None
        if party_id:
            return 1
        return super(Collection, self).exists(cursor, user, uri, context=context,
                cache=cache)

Collection()
