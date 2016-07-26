#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

import unittest
import json
import socket
from kubernetes import K8sObject, K8sConfig


class K8sObjectTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    # ------------------------------------------------------------------------------------- utils

    @staticmethod
    def _is_reachable(api_host):
        scheme, host, port = api_host.replace("//", "").split(':')
        try:
            s = socket.create_connection((host, port), timeout=1)
            s.close()
            return True
        except socket.timeout:
            return False

    # ------------------------------------------------------------------------------------- init

    def test_init_no_args(self):
        try:
            K8sObject()
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_init_with_invalid_config(self):
        config = object()
        try:
            K8sObject(config=config)
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_init_with_invalid_name(self):
        name = object()
        try:
            K8sObject(name=name)
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_init_invalid_object_type(self):
        ot = 666
        try:
            K8sObject(obj_type=ot)
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_init_unknown_object_type(self):
        ot = "yomama"
        try:
            K8sObject(obj_type=ot)
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_init_object_type_pod(self):
        ot = "Pod"
        name = "yomama"
        obj = K8sObject(name=name, obj_type=ot)
        self.assertIsInstance(obj, K8sObject)
        self.assertEqual(ot, obj.obj_type)
        self.assertEqual(name, obj.name)

    def test_init_object_type_rc(self):
        ot = "ReplicationController"
        name = "yomama"
        obj = K8sObject(name=name, obj_type=ot)
        self.assertIsInstance(obj, K8sObject)
        self.assertEqual(ot, obj.obj_type)
        self.assertEqual(name, obj.name)

    def test_init_object_type_secret(self):
        ot = "Secret"
        name = "yomama"
        obj = K8sObject(name=name, obj_type=ot)
        self.assertIsInstance(obj, K8sObject)
        self.assertEqual(ot, obj.obj_type)
        self.assertEqual(name, obj.name)

    def test_init_object_type_service(self):
        ot = "Service"
        name = "yomama"
        obj = K8sObject(name=name, obj_type=ot)
        self.assertIsInstance(obj, K8sObject)
        self.assertEqual(ot, obj.obj_type)
        self.assertEqual(name, obj.name)

    # ------------------------------------------------------------------------------------- conversions

    def test_object_as_dict(self):
        ot = "Service"
        name = "yomama"
        obj = K8sObject(name=name, obj_type=ot)
        dico = obj.as_dict()
        self.assertIsInstance(dico, dict)

    def test_object_as_json(self):
        ot = "Service"
        name = "yomama"
        obj = K8sObject(name=name, obj_type=ot)
        s = obj.as_json()
        self.assertIsInstance(s, str)
        valid = json.loads(s)
        self.assertIsInstance(valid, dict)

    # ------------------------------------------------------------------------------------- set

    def test_object_set_name(self):
        ot = "Pod"
        name1 = "yomama"
        obj = K8sObject(name=name1, obj_type=ot)
        self.assertEqual(name1, obj.name)
        name2 = "sofat"
        obj.set_name(name2)
        self.assertNotEqual(obj.name, name1)
        self.assertEqual(obj.name, name2)

    # ------------------------------------------------------------------------------------- api - list

    def test_object_pod_list_from_scratch(self):
        config = K8sConfig()
        if config.api_host is not None and self._is_reachable(config.api_host):
            ot = "Pod"
            name = "yomama"
            obj = K8sObject(name=name, obj_type=ot, config=config)
            r = obj.list()
            self.assertIsNotNone(r)
            self.assertEqual(0, len(r))

    def test_object_rc_list_from_scratch(self):
        config = K8sConfig()
        if config.api_host is not None and self._is_reachable(config.api_host):
            ot = "ReplicationController"
            name = "yomama"
            obj = K8sObject(name=name, obj_type=ot, config=config)
            r = obj.list()
            self.assertIsNotNone(r)
            self.assertEqual(0, len(r))

    def test_object_secret_list_from_scratch(self):
        config = K8sConfig()
        if config.api_host is not None and self._is_reachable(config.api_host):
            ot = "Secret"
            name = "yomama"
            obj = K8sObject(name=name, obj_type=ot, config=config)
            r = obj.list()
            self.assertIsNotNone(r)
            self.assertEqual(1, len(r))
            secret = r[0]
            self.assertIsInstance(secret, dict)
            self.assertEqual(3, len(secret))
            for i in ['data', 'metadata', 'type']:
                self.assertIn(i, secret)
            self.assertIsInstance(secret['data'], dict)
            self.assertIsInstance(secret['metadata'], dict)
            self.assertIsInstance(secret['type'], str)

    def test_object_service_list_from_scratch(self):
        config = K8sConfig()
        if config.api_host is not None and self._is_reachable(config.api_host):
            ot = "Service"
            name = "yomama"
            obj = K8sObject(name=name, obj_type=ot, config=config)
            r = obj.list()
            self.assertIsNotNone(r)
            self.assertEqual(1, len(r))
            service = r[0]
            self.assertIsInstance(service, dict)
            self.assertEqual(3, len(service))
            for i in ['metadata', 'spec', 'status']:
                self.assertIn(i, service)
                self.assertIsInstance(service[i], dict)
            for i in ['creationTimestamp', 'labels', 'name', 'namespace', 'resourceVersion', 'selfLink', 'uid']:
                self.assertIn(i, service['metadata'])
            for i in ['creationTimestamp', 'name', 'namespace', 'resourceVersion', 'selfLink', 'uid']:
                self.assertIsInstance(service['metadata'][i], str)
            self.assertIsInstance(service['metadata']['labels'], dict)
            self.assertEqual(2, len(service['metadata']['labels']))
            for i in ['component', 'provider']:
                self.assertIn(i, service['metadata']['labels'])
                self.assertIsInstance(service['metadata']['labels'][i], str)
            for i in ['clusterIP', 'ports', 'sessionAffinity', 'type']:
                self.assertIn(i, service['spec'])
            for i in ['clusterIP', 'sessionAffinity', 'type']:
                self.assertIsInstance(service['spec'][i], str)
            self.assertIsInstance(service['spec']['ports'], list)
            self.assertEqual(1, len(service['spec']['ports']))
            port = service['spec']['ports'][0]
            self.assertIsInstance(port, dict)
            self.assertEqual(4, len(port))
            for i in ['name', 'port', 'protocol', 'targetPort']:
                self.assertIn(i, port)
            for i in ['name', 'protocol']:
                self.assertIsInstance(port[i], str)
            for i in ['port', 'targetPort']:
                self.assertIsInstance(port[i], int)
