# -*- coding: utf-8 -*-
import json
import random

from django.conf.urls import patterns, url
from django.core.urlresolvers import reverse
from django.test import TestCase
from factory import Factory, SubFactory, Sequence

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
            'sColumns': '',
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
            'sColumns': '',
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
            'sColumns': '',
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
            'sColumns': '',
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
