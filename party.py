#This file is part of Tryton.  The COPYRIGHT file at the top level of
#this repository contains the full copyright notices and license terms.
from trytond.model import ModelSQL, ModelView
from trytond.report import Report
import base64
import copy

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
