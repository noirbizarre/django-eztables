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


class SpecialCase(models.Model):
    big_integer_field = models.BigIntegerField(default=1)
    boolean_field = models.BooleanField(default=True)
    char_field = models.CharField(max_length=128, blank=True)
    comma_separated_integer_field = models.CommaSeparatedIntegerField(max_length=5, blank=True)
    date_field = models.DateField(auto_now=True)
    datetime_field = models.DateTimeField(auto_now=True)
    decimal_field = models.DecimalField(decimal_places=2, max_digits=4, default='2.5')
    email_field = models.EmailField(max_length=128, blank=True)
    file_field = models.FileField(upload_to='to', blank=True)
    file_path_field = models.FilePathField(blank=True)
    float_field = models.FloatField(blank=True, default='2.5')
    generic_ip_address_field = models.GenericIPAddressField(default='0.0.0.0')
    image_field = models.ImageField(upload_to='to', blank=True)
    integer_field = models.IntegerField(default=1)
    ip_address_field = models.IPAddressField(default='0.0.0.0')
    null_boolean_field = models.NullBooleanField(default=True)
    positive_integer_field = models.PositiveIntegerField(default=1)
    positive_small_integer_field = models.PositiveSmallIntegerField(default=1)
    slug_field = models.SlugField(default='')
    small_integer_field = models.SmallIntegerField(default=1)
    text_field = models.TextField(blank=True)
    time_field = models.TimeField(auto_now=True)
    url_field = models.URLField(default='http://somewhere')
