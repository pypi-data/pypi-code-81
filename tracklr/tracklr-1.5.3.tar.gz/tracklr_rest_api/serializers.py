# -*- coding: utf-8 -*-
# vim: set expandtab tabstop=4 shiftwidth=4:

from rest_framework import serializers as s


class GroupStringSerializer(s.Serializer):
    group = s.CharField()


class GroupDecimalSerializer(s.Serializer):
    group = s.DecimalField(max_digits=18, decimal_places=2)


class LsStringSerializer(s.Serializer):
    date = s.DateField()
    summary = s.CharField()
    description = s.CharField()
    hours = s.DecimalField(max_digits=18, decimal_places=2)
    group = GroupStringSerializer(required=False, many=True)


class LsDecimalSerializer(s.Serializer):
    date = s.DateField()
    summary = s.CharField()
    description = s.CharField()
    hours = s.DecimalField(max_digits=18, decimal_places=2)
    group = GroupDecimalSerializer(required=False, many=True)
