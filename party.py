#This file is part of Tryton.  The COPYRIGHT file at the top level of
#this repository contains the full copyright notices and license terms.
from trytond.model import ModelSQL, ModelView, fields
from trytond.report import Report
from trytond.backend import TableHandler, FIELDS
import base64
import copy
import uuid


class Party(ModelSQL, ModelView):
    _name = 'party.party'
    uuid = fields.Char('UUID', required=True,
            help='Universally Unique Identifier')

    def __init__(self):
        super(Party, self).__init__()
        self._sql_constraints = [
                ('uuid_uniq', 'UNIQUE(uuid)',
                    'The UUID of the party must be unique!'),
        ]

    def init(self, cursor, module_name):
        table = TableHandler(cursor, self, module_name)

        if not table.column_exist('uuid'):
            table.add_raw_column('uuid',
                    FIELDS[self.uuid._type].sql_type(self.uuid),
                    FIELDS[self.uuid._type].sql_format, None, None)
            cursor.execute('SELECT id FROM "' + self._table + '"')
            for id, in cursor.fetchall():
                cursor.execute('UPDATE "' + self._table + '" ' \
                        'SET "uuid" = %s WHERE id = %s',
                        (self.default_uuid(cursor, 0), id))
        super(Party, self).init(cursor, module_name)

    def default_uuid(self, cursor, user, context=None):
        return str(uuid.uuid4())
Party()


class ActionReport(ModelSQL, ModelView):
    _name = 'ir.action.report'

    def __init__(self):
        super(ActionReport, self).__init__()
        new_ext = ('vcf', 'VCard file')
        if new_ext not in self.extension.selection:
            self.extension = copy.copy(self.extension)
            self.extension.selection.append(new_ext)
            self._reset_columns()

ActionReport()


class VCard(Report):
    _name = 'party_vcarddav.party.vcard'

    def execute(self, cursor, user, ids, datas, context=None):
        party_obj = self.pool.get('party.party')

        if context is None:
            context = {}

        parties = party_obj.browse(cursor, user, ids, context=context)

        data = ''.join(self.create_card(party).serialize() for party in parties)

        return ('vcf', base64.encodestring(data), False)

    def create_card(self, party):
        import vobject

        card = vobject.vCard()
        card.add('n')
        card.n.value = vobject.vcard.Name(party.name)
        card.add('fn')
        card.fn.value = party.full_name

        for address in party.addresses:
            country = address.country and address.country.name or ''
            subdivision = address.subdivision and address.subdivision.name or ''
            city = address.city or ''
            street = address.street and address.street + (
                address.streetbis and  (" " + address.streetbis) or '') or ''

            addr = card.add('adr')
            addr.value = vobject.vcard.Address(
                city=city, country=country, street=street, region=subdivision)

        for cm in party.contact_mechanisms:
            if cm.type == 'email':
                email = card.add('email')
                email.value = cm.value
                email.type_param = 'INTERNET'

            if cm.type == 'phone':
                phone = card.add('phone')
                phone.value = cm.value
                phone.type_param = 'WORK'

            if cm.type == 'mobile':
                mobile = card.add('phone')
                mobile.value = cm.value
                mobile.type_param = 'MOBILE'

        return card

VCard()
