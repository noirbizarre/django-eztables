# -*- coding: utf-8 -*-
from django import template
from djangojs.templatetags.js import js_lib, css


register = template.Library()


@register.simple_tag
def datatables_js():
    return js_lib('datatables/jquery.dataTables.min.js')


@register.simple_tag
def datatables_bootstrap_js():
    return js_lib('datatables/datatables.bootstrap.js')


@register.simple_tag
def datatables_bootstrap_css():
    return css('css/datatables.bootstrap.css')
