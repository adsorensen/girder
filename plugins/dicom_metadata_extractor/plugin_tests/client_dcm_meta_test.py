#!/usr/bin/env python
# -*- coding: utf-8 -*-

###############################################################################
#  Copyright Kitware Inc.
#
#  Licensed under the Apache License, Version 2.0 ( the "License" );
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
###############################################################################

import os.path
import sys

# Need to set the environment variable before importing Girder
os.environ['GIRDER_PORT'] = '31201'  # noqa

from girder.constants import ROOT_DIR
from server.dicom_metadata_extractor import ClientDicomMetadataExtractor
from tests import base
from . dicom_metadata_extractor_test import DicomMetadataExtractorTestCase


def setUpModule():
    base.startServer(False)


def tearDownModule():
    base.stopServer()


class ClientDicomMetadataExtractorTestCase(DicomMetadataExtractorTestCase):
    def testClientMetadataExtractor(self):
        item = self.model('item').load(self.item['_id'], user=self.user)
        self.assertEqual(item['name'], self.name)
        self.assertNotHasKeys(item, ['meta'])
        clientPath = os.path.join(ROOT_DIR, 'clients', 'python')
        sys.path.insert(0, clientPath)

        from girder_client import GirderClient

        client = GirderClient('localhost', int(os.environ['GIRDER_PORT']))
        client.authenticate(self.user['login'], self.password)
        extractor = ClientDicomMetadataExtractor(client, self.fileId, self.item['_id'])
        extractor.extractMetadata()
        sys.path.remove(clientPath)
        item = self.model('item').load(self.item['_id'], user=self.user)
        self.assertEqual(item['name'], self.name)
        self.assertHasKeys(item, ['meta'])
        self.assertEqual(item['meta']['Patient ID'], self.patientId)
