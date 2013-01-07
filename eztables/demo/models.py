# -*- coding: utf-8 -*-
from django.db import models


class Engine(models.Model):
    name = models.CharField(max_length=128)
    version = models.CharField(max_length=8, blank=True)
    css_grade = models.CharField(max_length=3)

    def __unicode__(self):
        return '%s %s (%s)' % (self.name, self.version or '-', self.css_grade)


class Browser(models.Model):
    name = models.CharField(max_length=128)
    platform = models.CharField(max_length=128)
    version = models.CharField(max_length=8, blank=True)
    engine = models.ForeignKey(Engine)

    def __unicode__(self):
        return '%s %s' % (self.name, self.version or '-')
