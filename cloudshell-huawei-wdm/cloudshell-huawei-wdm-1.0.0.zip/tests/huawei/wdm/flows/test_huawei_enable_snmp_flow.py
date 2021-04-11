#!/usr/bin/python
# -*- coding: utf-8 -*-

from unittest import TestCase

from cloudshell.huawei.wdm.flows.huawei_enable_snmp_flow import HuaweiWDMEnableSnmpFlow


class TestHuaweiWDMEnableSNMPFlow(TestCase):
    def test_import(self):
        self.assertTrue(HuaweiWDMEnableSnmpFlow)
