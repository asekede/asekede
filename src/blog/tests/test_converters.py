from django.test import TestCase

from blog.converters import TwoDigitDayConverter, TwoDigitMonthConverter, FourDigitYearConverter

import re

class TwoDigitDayConverterTestCase(TestCase):
    def test_to_python(self):
        converter = TwoDigitDayConverter() 
        day = re.match(converter.regex, '07').string
        self.assertEqual(converter.to_python(day), 7)
        day = re.match(converter.regex, '10').string
        self.assertEqual(converter.to_python(day), 10)

    def test_to_url(self):
        converter = TwoDigitDayConverter() 
        day = re.match(converter.regex, '07').string
        self.assertEqual(converter.to_url(day), '07') 
        day = re.match(converter.regex, '10').string
        self.assertEqual(converter.to_url(day), '10')


class TwoDigitMonthConverterTestCase(TestCase):
    def test_to_python(self):
        converter = TwoDigitMonthConverter() 
        month = re.match(converter.regex, '01').string
        self.assertEqual(converter.to_python(month), 1)
        month = re.match(converter.regex, '10').string
        self.assertEqual(converter.to_python(month), 10)

    def test_to_url(self):
        converter = TwoDigitMonthConverter() 
        month = re.match(converter.regex, '01').string
        self.assertEqual(converter.to_url(month), '01')
        month = re.match(converter.regex, '10').string
        self.assertEqual(converter.to_url(month), '10')


class FourDigitYearConverterTestCase(TestCase):
    def test_to_python(self):
        converter = FourDigitYearConverter() 
        year = re.match(converter.regex, '1994').string
        self.assertEqual(converter.to_python(year), 1994)

    def test_to_url(self):
        converter = FourDigitYearConverter() 
        year = re.match(converter.regex, '1994').string
        self.assertEqual(converter.to_url(year), '1994')
