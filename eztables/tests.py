# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
import random

from django import forms
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils import unittest

from django.utils.six import iteritems
from django.utils.six.moves import xrange
from factory import DjangoModelFactory, SubFactory, Sequence

from eztables.forms import DatatablesForm
from eztables.views import RE_FORMATTED
from eztables.demo.models import Browser, Engine, SpecialCase
from eztables.demo.views import SpecialCaseDatatablesView


class EngineFactory(DjangoModelFactory):
    FACTORY_FOR = Engine
    name = random.choice(('Gecko', 'Webkit', 'Presto'))
    version = Sequence(lambda n: n)
    css_grade = random.choice(('A', 'C', 'X'))


class BrowserFactory(DjangoModelFactory):
    FACTORY_FOR = Browser
    name = random.choice(('Firefox', 'Safari', 'Chrome'))
    platform = random.choice(('Windows', 'MacOSX', 'Linux'))
    version = Sequence(lambda n: n)
    engine = SubFactory(EngineFactory)


class SpecialCaseFactory(DjangoModelFactory):
    FACTORY_FOR = SpecialCase

UNSUPPORTED_LOOKUP_FIELDS = (
    'big_integer_field',
    'boolean_field',
    'decimal_field',
    'float_field',
    'integer_field',
    'null_boolean_field',
    'positive_integer_field',
    'positive_small_integer_field',
    'small_integer_field',
)


class DatatablesFormTest(unittest.TestCase):
    def test_base_parameters(self):
        '''Should validate base parameters'''
        form = DatatablesForm({
            'sEcho': '1',
            'iColumns': '5',
            'iDisplayStart': '0',
            'iDisplayLength': '10',
            'sSearch': '',
            'bRegex': 'false',
            'iSortingCols': '1',
            'iSortCol_0': '0',
            'sSortDir_0': 'asc',
        })
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['sEcho'], '1')
        self.assertEqual(form.cleaned_data['iColumns'], 5)
        self.assertEqual(form.cleaned_data['iDisplayStart'], 0)
        self.assertEqual(form.cleaned_data['iDisplayLength'], 10)
        self.assertEqual(form.cleaned_data['sSearch'], '')
        self.assertEqual(form.cleaned_data['bRegex'], False)
        self.assertEqual(form.cleaned_data['iSortingCols'], 1)

    def test_dyanmic_extra_parameters(self):
        '''Should dynamiclly add extra parameters'''
        form = DatatablesForm({
            'sEcho': '1',
            'iColumns': '5',
            'iDisplayStart': '0',
            'iDisplayLength': '10',
            'sSearch': '',
            'bRegex': 'false',
            'iSortingCols': '2',
        })

        for i in xrange(5):
            self.assertTrue('mDataProp_%s' % i in form.fields)
            self.assertTrue(isinstance(form['mDataProp_%s' % i].field, forms.CharField))
            self.assertFalse(form['mDataProp_%s' % i].field.required)

            self.assertTrue('sSearch_%s' % i in form.fields)
            self.assertTrue(isinstance(form['sSearch_%s' % i].field, forms.CharField))
            self.assertFalse(form['sSearch_%s' % i].field.required)

            self.assertTrue('bRegex_%s' % i in form.fields)
            self.assertTrue(isinstance(form['bRegex_%s' % i].field, forms.BooleanField))
            self.assertFalse(form['bRegex_%s' % i].field.required)

            self.assertTrue('bSearchable_%s' % i in form.fields)
            self.assertTrue(isinstance(form['bSearchable_%s' % i].field, forms.BooleanField))
            self.assertFalse(form['bSearchable_%s' % i].field.required)

            self.assertTrue('bSortable_%s' % i in form.fields)
            self.assertTrue(isinstance(form['bSortable_%s' % i].field, forms.BooleanField))
            self.assertFalse(form['bSortable_%s' % i].field.required)

        for i in xrange(2):
            self.assertTrue('iSortCol_%s' % i in form.fields)
            self.assertTrue(isinstance(form['iSortCol_%s' % i].field, forms.IntegerField))
            self.assertTrue(form['iSortCol_%s' % i].field.required)

            self.assertTrue('sSortDir_%s' % i in form.fields)
            self.assertTrue(isinstance(form['sSortDir_%s' % i].field, forms.ChoiceField))
            self.assertTrue(form['sSortDir_%s' % i].field.required)

        self.assertFalse('iSortCol_2' in form.fields)

    def test_valid_extra_parameters(self):
        '''Should validate with extra parameters'''
        form = DatatablesForm({
            'sEcho': '1',
            'iColumns': '5',
            'iDisplayStart': '0',
            'iDisplayLength': '10',
            'sSearch': '',
            'bRegex': 'false',
            'iSortingCols': '1',
            'mDataProp_0': '0',
            'mDataProp_1': '1',
            'mDataProp_2': '2',
            'mDataProp_3': '3',
            'mDataProp_4': '4',
            'sSearch_0': 's0',
            'sSearch_1': 's1',
            'sSearch_2': 's2',
            'sSearch_3': 's3',
            'sSearch_4': 's4',
            'bRegex_0': 'false',
            'bRegex_1': 'false',
            'bRegex_2': 'false',
            'bRegex_3': 'false',
            'bRegex_4': 'false',
            'bSearchable_0': 'true',
            'bSearchable_1': 'true',
            'bSearchable_2': 'true',
            'bSearchable_3': 'true',
            'bSearchable_4': 'true',
            'bSortable_0': 'true',
            'bSortable_1': 'true',
            'bSortable_2': 'true',
            'bSortable_3': 'true',
            'bSortable_4': 'true',
            'iSortCol_0': '0',
            'sSortDir_0': 'asc',
        })
        self.assertTrue(form.is_valid())
        for idx in xrange(5):
            self.assertEqual(form.cleaned_data['mDataProp_%s' % idx], '%s' % idx)
            self.assertEqual(form.cleaned_data['sSearch_%s' % idx], 's%s' % idx)
            self.assertEqual(form.cleaned_data['bRegex_%s' % idx], False)
            self.assertEqual(form.cleaned_data['bSearchable_%s' % idx], True)
            self.assertEqual(form.cleaned_data['bSortable_%s' % idx], True)
        self.assertEqual(form.cleaned_data['iSortCol_0'], 0)
        self.assertEqual(form.cleaned_data['sSortDir_0'], 'asc')

    def test_invalid_sorting_parameters(self):
        '''Should not validate invalid sorting parameters'''
        form = DatatablesForm({
            'sEcho': '1',
            'iColumns': '5',
            'iDisplayStart': '0',
            'iDisplayLength': '10',
            'sSearch': '',
            'bRegex': 'false',
            'iSortingCols': '1',
        })
        self.assertFalse(form.is_valid())


class FormattedFieldRegexTest(unittest.TestCase):
    def test_not_formatted(self):
        '''Should not match unformatted field descriptions'''
        self.assertIsNone(RE_FORMATTED.match('my_field'))

    def test_formatted_single_token(self):
        '''Should match a formatted field description with a single token'''
        matches = RE_FORMATTED.findall('{field}')
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0], 'field')

    def test_formatted_multi_token(self):
        '''Should match a formatted field description with a single token'''
        matches = RE_FORMATTED.findall('{field_0}-{field_1}: {field_2}')
        self.assertEqual(len(matches), 3)
        for i in xrange(3):
            self.assertEqual(matches[i], 'field_%s' % i)

    def test_formatted_nester_token(self):
        '''Should match a formatted field description with a single token'''
        matches = RE_FORMATTED.findall('{nested__field_0}-{nested__field_1}: {nested__field_2}')
        self.assertEqual(len(matches), 3)
        for i in xrange(3):
            self.assertEqual(matches[i], 'nested__field_%s' % i)


ENGINE_NAME, NAME, VERSION, PLATFORM, ENGINE_VERSION, ENGINE_CSS_GRADE = range(6)


class DatatablesTestMixin(object):

    def get_response(self, name, data={}):
        raise NotImplemented

    def value(self, row, field_id):
        raise NotImplemented

    def assertInstance(self, row):
        raise NotImplemented

    def build_query(self, **kwargs):
        query = {
            'sEcho': '1',
            'iColumns': '5',
            'iDisplayStart': '0',
            'iDisplayLength': '10',
            'sSearch': '',
            'bRegex': 'false',
            'mDataProp_0': '0',
            'mDataProp_1': '1',
            'mDataProp_2': '2',
            'mDataProp_3': '3',
            'mDataProp_4': '4',
            'sSearch_0': '',
            'sSearch_1': '',
            'sSearch_2': '',
            'sSearch_3': '',
            'sSearch_4': '',
            'bRegex_0': 'false',
            'bRegex_1': 'false',
            'bRegex_2': 'false',
            'bRegex_3': 'false',
            'bRegex_4': 'false',
            'bSearchable_0': 'true',
            'bSearchable_1': 'true',
            'bSearchable_2': 'true',
            'bSearchable_3': 'true',
            'bSearchable_4': 'true',
            'bSortable_0': 'true',
            'bSortable_1': 'true',
            'bSortable_2': 'true',
            'bSortable_3': 'true',
            'bSortable_4': 'true',
            'iSortingCols': '1',
            'iSortCol_0': '0',
            'sSortDir_0': 'asc',
        }
        query.update(kwargs)
        return query

    def build_query_special(self, **kwargs):
        query = {
            'sEcho': '1',
            'iColumns': len(SpecialCaseDatatablesView.fields),
            'iDisplayStart': '0',
            'iDisplayLength': '10',
            'sSearch': '',
            'bRegex': 'false',
            'iSortingCols': '1',
            'iSortCol_0': '0',
            'sSortDir_0': 'asc',
        }

        for idx, field in enumerate(SpecialCaseDatatablesView.fields):
            query.update({
                'mDataProp_%s' % idx: '%s' % idx,
                'sSearch_%s' % idx: '',
                'bRegex_%s' % idx: 'false',
                'bSearchable_%s' % idx: 'true',
                'bSortable_%s' % idx: 'true',
            })
        query.update(kwargs)
        return query

    def test_empty(self):
        '''Should return an empty Datatables JSON response'''
        response = self.get_response('browsers', self.build_query())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')

        data = json.loads(response.content.decode())
        self.assertTrue('iTotalRecords' in data)
        self.assertEqual(data['iTotalRecords'], 0)
        self.assertTrue('iTotalDisplayRecords' in data)
        self.assertEqual(data['iTotalDisplayRecords'], 0)
        self.assertTrue('sEcho' in data)
        self.assertEqual(data['sEcho'], '1')
        self.assertTrue('aaData' in data)
        self.assertEqual(len(data['aaData']), 0)

    def test_unpaginated(self):
        '''Should return an unpaginated Datatables JSON response'''
        browsers = [BrowserFactory() for _ in xrange(5)]

        response = self.get_response('browsers', self.build_query())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')

        data = json.loads(response.content.decode())
        self.assertTrue('iTotalRecords' in data)
        self.assertEqual(data['iTotalRecords'], len(browsers))
        self.assertTrue('iTotalDisplayRecords' in data)
        self.assertEqual(data['iTotalDisplayRecords'], len(browsers))
        self.assertTrue('sEcho' in data)
        self.assertEqual(data['sEcho'], '1')
        self.assertTrue('aaData' in data)
        self.assertEqual(len(data['aaData']), len(browsers))
        for row in data['aaData']:
            self.assertInstance(row)

    def test_paginated(self):
        '''Should return a paginated Datatables JSON response'''
        browsers = [BrowserFactory() for _ in xrange(15)]

        response = self.get_response('browsers', self.build_query())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')

        data = json.loads(response.content.decode())
        self.assertTrue('iTotalRecords' in data)
        self.assertEqual(data['iTotalRecords'], len(browsers))
        self.assertTrue('iTotalDisplayRecords' in data)
        self.assertEqual(data['iTotalDisplayRecords'], len(browsers))
        self.assertTrue('sEcho' in data)
        self.assertEqual(data['sEcho'], '1')
        self.assertTrue('aaData' in data)
        self.assertEqual(len(data['aaData']), 10)
        for row in data['aaData']:
            self.assertInstance(row)

    def test_formatted(self):
        '''Should return an formatted Datatables JSON response'''
        browsers = [BrowserFactory() for _ in xrange(15)]

        response = self.get_response('formatted-browsers', self.build_query())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')

        data = json.loads(response.content.decode())
        self.assertTrue('iTotalRecords' in data)
        self.assertEqual(data['iTotalRecords'], len(browsers))
        self.assertTrue('iTotalDisplayRecords' in data)
        self.assertEqual(data['iTotalDisplayRecords'], len(browsers))
        self.assertTrue('sEcho' in data)
        self.assertEqual(data['sEcho'], '1')
        self.assertTrue('aaData' in data)
        self.assertEqual(len(data['aaData']), 10)
        for row in data['aaData']:
            self.assertInstance(row)

    def test_unicode(self):
        '''Should handle unicode special caracters'''
        BrowserFactory(name='é€ç')

        response = self.get_response('formatted-browsers', self.build_query())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')

        data = json.loads(response.content.decode())
        self.assertEqual(len(data['aaData']), 1)
        self.assertInstance(data['aaData'][0])

    def test_sorted_single_field(self):
        '''Should handle sorting on a single field'''
        for i in xrange(5):
            BrowserFactory(name='Browser %s' % i)

        response = self.get_response('browsers', self.build_query(iSortCol_0=1, sSortDir_0='desc'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')

        data = json.loads(response.content.decode())
        for idx, row in enumerate(data['aaData']):
            field_value = self.value(row, NAME)
            self.assertEqual(field_value, 'Browser %s' % (4 - idx))

    def test_sorted_multiple_field(self):
        '''Should handle sorting on multiple field'''
        for i in xrange(10):
            BrowserFactory(name='Browser %s' % (i // 2), engine__version='%s' % i)

        response = self.get_response('browsers', self.build_query(
            iSortingCols=2,
            iSortCol_0=1,
            sSortDir_0='desc',
            iSortCol_1=3,
            sSortDir_1='asc'
        ))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')

        data = json.loads(response.content.decode())
        expected = (
            ('Browser 4', '8'),
            ('Browser 4', '9'),
            ('Browser 3', '6'),
            ('Browser 3', '7'),
            ('Browser 2', '4'),
            ('Browser 2', '5'),
            ('Browser 1', '2'),
            ('Browser 1', '3'),
            ('Browser 0', '0'),
            ('Browser 0', '1'),
        )
        for idx, row in enumerate(data['aaData']):
            expected_name, expected_version = expected[idx]
            self.assertEqual(self.value(row, NAME), expected_name)
            self.assertEqual(self.value(row, ENGINE_VERSION), expected_version)

    def test_sorted_formatted(self):
        '''Should handle sorting with formatting'''
        for i in xrange(10):
            BrowserFactory(name='Browser %s' % (i // 2), version='%s' % i)

        response = self.get_response('formatted-browsers', self.build_query(iSortCol_0=1, sSortDir_0='desc'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')

        data = json.loads(response.content.decode())
        expected = (
            'Browser 4 9',
            'Browser 4 8',
            'Browser 3 7',
            'Browser 3 6',
            'Browser 2 5',
            'Browser 2 4',
            'Browser 1 3',
            'Browser 1 2',
            'Browser 0 1',
            'Browser 0 0',
        )
        for idx, row in enumerate(data['aaData']):
            self.assertEqual(self.value(row, NAME), expected[idx])

    def test_sorted_custom_implementation(self):
        '''Should handle sorting with a custom implementation'''
        for i in xrange(5):
            BrowserFactory(name='Browser %s' % i, version='%s' % (5 - i))

        response = self.get_response('custom-browsers', self.build_query(iSortCol_0=1, sSortDir_0='desc'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')

        data = json.loads(response.content.decode())
        for idx, row in enumerate(data['aaData']):
            field_value = self.value(row, NAME)
            self.assertEqual(field_value, 'Browser %s' % idx)

    def test_sorted_custom_implementation_many_fields(self):
        '''Should handle sorting with a custom implementation on many fields'''
        for i in xrange(5):
            BrowserFactory(name='Browser %s' % i, platform='%s' % (5 - i))

        response = self.get_response('custom-browsers', self.build_query(iSortCol_0=3, sSortDir_0='asc'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')

        data = json.loads(response.content.decode())
        for idx, row in enumerate(data['aaData']):
            field_value = self.value(row, NAME)
            self.assertEqual(field_value, 'Browser %s' % idx)

    def test_global_search_single_term(self):
        '''Should do a global search on a single term'''
        for _ in xrange(2):
            BrowserFactory(name='test')
        for _ in xrange(3):
            BrowserFactory(engine__name='engine')

        response = self.get_response('browsers', self.build_query(sSearch='test'))
        data = json.loads(response.content.decode())
        self.assertEqual(len(data['aaData']), 2)
        for row in data['aaData']:
            self.assertEqual(self.value(row, NAME), 'test')

        response = self.get_response('browsers', self.build_query(sSearch='engine'))
        data = json.loads(response.content.decode())
        self.assertEqual(len(data['aaData']), 3)
        for row in data['aaData']:
            self.assertEqual(self.value(row, ENGINE_NAME), 'engine')

    def test_global_search_many_terms(self):
        '''Should do a global search on many terms'''
        for _ in xrange(2):
            BrowserFactory(name='test')
        for _ in xrange(3):
            BrowserFactory(engine__name='engine')
        for _ in xrange(4):
            BrowserFactory(name='test', engine__name='engine')

        response = self.get_response('browsers', self.build_query(sSearch='test engine'))
        data = json.loads(response.content.decode())
        self.assertEqual(len(data['aaData']), 4)
        for row in data['aaData']:
            self.assertEqual(self.value(row, ENGINE_NAME), 'engine')
            self.assertEqual(self.value(row, NAME), 'test')

    def test_global_search_regex(self):
        '''Should do a global search on a regex'''
        for _ in xrange(3):
            BrowserFactory()
        for _ in xrange(2):
            BrowserFactory(name='test')

        response = self.get_response('browsers', self.build_query(sSearch='[tes]{4}', bRegex=True))
        data = json.loads(response.content.decode())
        self.assertEqual(len(data['aaData']), 2)
        for row in data['aaData']:
            self.assertEqual(self.value(row, NAME), 'test')

    def test_column_search_single_column(self):
        '''Should filter on a single column'''
        for _ in xrange(3):
            BrowserFactory()
        for _ in xrange(2):
            BrowserFactory(name='test')

        response = self.get_response('browsers', self.build_query(sSearch_1='tes'))
        data = json.loads(response.content.decode())
        self.assertEqual(len(data['aaData']), 2)
        for row in data['aaData']:
            self.assertEqual(self.value(row, NAME), 'test')

    def test_column_search_many_columns(self):
        '''Should filter on many columns'''
        for _ in xrange(2):
            BrowserFactory(name='test')
        for _ in xrange(3):
            BrowserFactory(engine__name='engine')
        for _ in xrange(4):
            BrowserFactory(name='test', engine__name='engine')

        response = self.get_response('browsers', self.build_query(sSearch_0='eng', sSearch_1='tes'))
        data = json.loads(response.content.decode())
        self.assertEqual(len(data['aaData']), 4)
        for row in data['aaData']:
            self.assertEqual(self.value(row, ENGINE_NAME), 'engine')
            self.assertEqual(self.value(row, NAME), 'test')

    def test_column_search_formatted_column(self):
        '''Should filter on a formatted column'''
        for _ in xrange(3):
            BrowserFactory()
        for _ in xrange(2):
            BrowserFactory(name='test')

        response = self.get_response('formatted-browsers', self.build_query(sSearch_1='tes'))
        data = json.loads(response.content.decode())
        self.assertEqual(len(data['aaData']), 2)
        for row in data['aaData']:
            self.assertTrue(self.value(row, NAME).startswith('test'))

    def test_column_search_regex(self):
        '''Should filter on a single column with regex'''
        for _ in xrange(3):
            BrowserFactory()
        for _ in xrange(2):
            BrowserFactory(name='test')

        response = self.get_response('browsers', self.build_query(sSearch_1='[tes]{4}', bRegex_1=True))
        data = json.loads(response.content.decode())
        self.assertEqual(len(data['aaData']), 2)
        for row in data['aaData']:
            self.assertEqual(self.value(row, NAME), 'test')

    def test_column_search_custom(self):
        '''Should filter on a single column with custom search'''
        for i in xrange(3):
            BrowserFactory(version='%s.%s' % (i, i))
        for _ in xrange(2):
            BrowserFactory(name='test')

        response = self.get_response('custom-browsers', self.build_query(sSearch_1='tes'))
        data = json.loads(response.content.decode())
        self.assertEqual(len(data['aaData']), 0)
        for row in data['aaData']:
            self.assertEqual(self.value(row, NAME), 'test')

        response = self.get_response('custom-browsers', self.build_query(sSearch_1='1.1'))
        data = json.loads(response.content.decode())
        self.assertEqual(len(data['aaData']), 1)
        for row in data['aaData']:
            self.assertNotEqual(self.value(row, NAME), 'test')

    def test_global_search_regex_unsupported_fields(self):
        '''Should not fail performing global regex search with unsupported fields'''
        for _ in range(3):
            SpecialCaseFactory()

        response = self.get_response('special', self.build_query_special(sSearch='^a$', bRegex=True))
        data = json.loads(response.content.decode())
        self.assertEqual(len(data['aaData']), 0)

    def test_column_search_regex_unsupported_fields(self):
        '''Should not fail performing regex search on unsupported column field'''
        for _ in range(3):
            SpecialCaseFactory()

        for idx, field in enumerate(SpecialCaseDatatablesView.fields):
            params = {'sSearch_%s' % idx: '^a$', 'bRegex_%s' % idx: True}
            response = self.get_response('special', self.build_query_special(**params))
            data = json.loads(response.content.decode())
            self.assertEqual(len(data['aaData']), 3 if field in UNSUPPORTED_LOOKUP_FIELDS else 0)


class ArrayMixin(object):
    urls = 'eztables.test_array_urls'

    def value(self, row, field_id):
        return row[field_id]

    def assertInstance(self, row):
        self.assertTrue(isinstance(row, list))
        self.assertEqual(len(row), 6)


class ObjectMixin(object):
    urls = 'eztables.test_object_urls'

    id_to_name = {
        0: 'engine',
        1: 'name',
        2: 'platform',
        3: 'version',
        4: 'engine_version',
        5: 'css_grade',
    }

    def build_query(self, **kwargs):
        query = super(ObjectMixin, self).build_query(**kwargs)
        query.update(dict((
            ('mDataProp_%s' % k, v) for k, v in iteritems(self.id_to_name)
        )))
        return query

    def value(self, row, field_id):
        return row[self.id_to_name[field_id]]

    def assertInstance(self, row):
        self.assertTrue(isinstance(row, dict))
        for key in self.id_to_name.values():
            self.assertTrue(key in row)


class GetMixin(object):
    def get_response(self, name, data={}):
        return self.client.get(reverse(name), data)


class PostMixin(object):
    def get_response(self, name, data={}):
        return self.client.post(reverse(name), data)


class DatatablesArrayGetTest(ArrayMixin, GetMixin, DatatablesTestMixin, TestCase):
    pass


class DatatablesArrayPostTest(ArrayMixin, PostMixin, DatatablesTestMixin, TestCase):
    pass


class DatatablesObjGetTest(ObjectMixin, GetMixin, DatatablesTestMixin, TestCase):
    pass


class DatatablesObjPostTest(ObjectMixin, PostMixin, DatatablesTestMixin, TestCase):
    pass
