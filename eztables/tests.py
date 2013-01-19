# -*- coding: utf-8 -*-
import json
import random
import unittest

from django import forms
from django.conf.urls import patterns, url
from django.core.urlresolvers import reverse
from django.test import TestCase
from factory import Factory, SubFactory, Sequence

from eztables.forms import DatatablesForm
from eztables.demo.models import Browser, Engine
from eztables.demo.views import BrowserDatatablesView, AdaptedBrowserDatatablesView


class EngineFactory(Factory):
    FACTORY_FOR = Engine
    name = random.choice(('Gecko', 'Webkit', 'Presto'))
    version = Sequence(lambda n: n)
    css_grade = random.choice(('A', 'C', 'X'))


class BrowserFactory(Factory):
    FACTORY_FOR = Browser
    name = random.choice(('Firefox', 'Safari', 'Chrome'))
    platform = random.choice(('Windows', 'MacOSX', 'Linux'))
    version = Sequence(lambda n: n)
    engine = SubFactory(EngineFactory)


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
            self.assertFalse(form['iSortCol_%s' % i].field.required)

            self.assertTrue('sSortDir_%s' % i in form.fields)
            self.assertTrue(isinstance(form['sSortDir_%s' % i].field, forms.ChoiceField))
            self.assertFalse(form['sSortDir_%s' % i].field.required)

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
            'iSortCol_0': '0',
            'sSortDir_0': 'asc',
        })
        self.assertTrue(form.is_valid())


class DatatablesTestMixin(object):
    urls = patterns('',
        url(r'^$', BrowserDatatablesView.as_view(), name='browsers'),
        url(r'^adapted/$', AdaptedBrowserDatatablesView.as_view(), name='adapted-browsers'),
    )

    def get_response(self, name, data={}):
        raise NotImplemented

    def test_empty_response(self):
        '''Should return an empty Datatables JSON response'''
        response = self.get_response('browsers', {
            'sEcho': '1',
            'iColumns': '5',
            'iDisplayStart': '0',
            'iDisplayLength': '10',
            'sSearch': '',
            'bRegex': 'false',
            'iSortingCols': '1',
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')

        data = json.loads(response.content)
        self.assertTrue('iTotalRecords' in data)
        self.assertEqual(data['iTotalRecords'], 0)
        self.assertTrue('iTotalDisplayRecords' in data)
        self.assertEqual(data['iTotalDisplayRecords'], 0)
        self.assertTrue('sEcho' in data)
        self.assertEqual(data['sEcho'], '1')
        self.assertTrue('aaData' in data)
        self.assertEqual(len(data['aaData']), 0)

    def test_unpaginated_response(self):
        browsers = [BrowserFactory() for _ in xrange(5)]

        response = self.get_response('browsers', {
            'sEcho': '1',
            'iColumns': '5',
            'iDisplayStart': '0',
            'iDisplayLength': '10',
            'sSearch': '',
            'bRegex': 'false',
            'iSortingCols': '1',
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')

        data = json.loads(response.content)
        self.assertTrue('iTotalRecords' in data)
        self.assertEqual(data['iTotalRecords'], len(browsers))
        self.assertTrue('iTotalDisplayRecords' in data)
        self.assertEqual(data['iTotalDisplayRecords'], len(browsers))
        self.assertTrue('sEcho' in data)
        self.assertEqual(data['sEcho'], '1')
        self.assertTrue('aaData' in data)
        self.assertEqual(len(data['aaData']), len(browsers))
        for row in data['aaData']:
            self.assertEqual(len(row), 5)

    def test_paginated_response(self):
        browsers = [BrowserFactory() for _ in xrange(15)]

        response = self.get_response('browsers', {
            'sEcho': '1',
            'iColumns': '5',
            'iDisplayStart': '0',
            'iDisplayLength': '10',
            'sSearch': '',
            'bRegex': 'true',
            'iSortingCols': '1',
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')

        data = json.loads(response.content)
        self.assertTrue('iTotalRecords' in data)
        self.assertEqual(data['iTotalRecords'], len(browsers))
        self.assertTrue('iTotalDisplayRecords' in data)
        self.assertEqual(data['iTotalDisplayRecords'], len(browsers))
        self.assertTrue('sEcho' in data)
        self.assertEqual(data['sEcho'], '1')
        self.assertTrue('aaData' in data)
        self.assertEqual(len(data['aaData']), 10)
        for row in data['aaData']:
            self.assertEqual(len(row), 5)

    def test_adapted_response(self):
        browsers = [BrowserFactory() for _ in xrange(15)]

        response = self.get_response('adapted-browsers', {
            'sEcho': '1',
            'iColumns': '5',
            'iDisplayStart': '0',
            'iDisplayLength': '10',
            'sSearch': '',
            'bRegex': 'true',
            'iSortingCols': '1',
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')

        data = json.loads(response.content)
        self.assertTrue('iTotalRecords' in data)
        self.assertEqual(data['iTotalRecords'], len(browsers))
        self.assertTrue('iTotalDisplayRecords' in data)
        self.assertEqual(data['iTotalDisplayRecords'], len(browsers))
        self.assertTrue('sEcho' in data)
        self.assertEqual(data['sEcho'], '1')
        self.assertTrue('aaData' in data)
        self.assertEqual(len(data['aaData']), 10)
        for row in data['aaData']:
            self.assertEqual(len(row), 5)


class DatatablesGetTest(DatatablesTestMixin, TestCase):
    def get_response(self, name, data={}):
        return self.client.get(reverse(name), data)


class DatatablesPostTest(DatatablesTestMixin, TestCase):
    def get_response(self, name, data={}):
        return self.client.post(reverse(name), data)
