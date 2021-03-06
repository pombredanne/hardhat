import os
import nose.tools as n
import usps

class TestParse:
    def _(self, fixture, expected):
        observed = usps._parse(open(self._fixture(fixture)).read())
        n.assert_list_equal(observed, expected)

    @staticmethod
    def _fixture(filename):
        return os.path.join('fixtures', 'usps', filename)

    def test_multiple_results(self):
        self._('ZipLookupResultsAction!input.action?city=Washington&zip=20500&companyName=&address1=1600+Pennsylvania+Avenue+NW&address2=&postalCode=&state=DC&resultMode=0&urbanCode=', [
            {u"city": u"WASHINGTON", u"state": u"DC", u"address1": u"1600 PENNSYLVANIA AVE NW", u"zip": u"20500", u"zip4": u"0003"},
            {u"city": u"WASHINGTON", u"name": u"WHITE HOUSE", u"zip": u"20500", u"address1": u"1600 PENNSYLVANIA AVE NW", "state": u"DC", u"zip4": u"0003"},
            {u"city": u"WASHINGTON", u"name": u"PRESIDENT", u"zip": u"20500", u"address1": u"1600 PENNSYLVANIA AVE NW", "state": u"DC", u"zip4": u"0001"},
            {u"city": u"WASHINGTON", u"name": u"FIRST LADY", u"zip": u"20500", u"address1": u"1600 PENNSYLVANIA AVE NW", "state": u"DC", u"zip4": u"0002"},
            {u"city": u"WASHINGTON", u"name": u"THE WHITE HOUSE", u"zip": u"20500", u"address1": u"1600 PENNSYLVANIA AVE NW", "state": u"DC", u"zip4": u"0004"},
            {u"city": u"WASHINGTON", u"state": u"DC", u"address1": u"1600 PENNSYLVANIA AVE NW", u"zip": u"20500", u"zip4": u"0005"},
            {u"city": u"WASHINGTON", u"name": u"GREETINGS OFFICE", u"zip": u"20500", u"address1": u"1600 PENNSYLVANIA AVE NW", "state": u"DC", u"zip4": u"0039"},
            {u"city": u"WASHINGTON", u"name": u"WHITE HOUSE STATION", u"zip": u"20500", u"address1": u"1600 PENNSYLVANIA AVE NW", "state": u"DC", u"zip4": u"0049"},
            {u"city": u"WASHINGTON", u"name": u"AMER FUND FOR AFGHAN CHILD", u"zip": u"20500", u"address1": u"1600 PENNSYLVANIA AVE NW", "state": u"DC", u"zip4": u"1600"},
        ])

#   def test_no_results(self):
#       self._('', [])

    def test_one_result(self):
        self._('ZipLookupResultsAction!input.action?resultMode=0&companyName=&address1=19+Bayhill+RD&address2=&city=Dellwood&state=MN&urbanCode=&postalCode=&zip=55110', [{
            u'address1': u'19 BAYHILL RD',
            u'city': u'DELLWOOD',
            u'state': u'MN',
            u'zip': u'55110',
            u'zip4': u'6178',
        }])

    def test_not_found(self):
        self._('ZipLookupResultsAction!input.action?city=GOLDEN+VALLEY&state=MN&postalCode=&urbanCode=&companyName=&resultMode=0&address1=5307+CIR+DOWN&address2=203&zipcode=55416', [])

    def test_not_recognized(self):
        self._('ZipLookupResultsAction!input.action?resultMode=0&companyName=&address1=26130+Birch+AVE&address2=&city=Ni%0Asswa&state=MN&urbanCode=&postalCode=&zip=56468', [])

    def test_not_found2(self):
        self._('ZipLookupResultsAction!input.action?city=None&state=MN&postalCode=&urbanCode=&companyName=&resultMode=0&address1=1972+Timber+Wolf+TRL+S&address2=&zipcode=55122', [])


def test_white_house():
    observed = usps.lookup(u"1600 PENNSYLVANIA AVE NW", u'', u'Washington', u'DC', u"20500")
    n.assert_equal(type(observed), list)
    n.assert_equal(len(observed), 10)
