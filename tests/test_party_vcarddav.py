# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.
import unittest
import trytond.tests.test_tryton
from trytond.tests.test_tryton import test_depends


class PartyVCardDAVTestCase(unittest.TestCase):
    'Test PartyVCardDAV module'

    def setUp(self):
        trytond.tests.test_tryton.install_module('party_vcarddav')

    def test0006depends(self):
        'Test depends'
        test_depends()


def suite():
    suite = trytond.tests.test_tryton.suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
            PartyVCardDAVTestCase))
    return suite
