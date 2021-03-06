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

from tests import base
from girder.constants import ROOT_DIR


class DicomMetadataExtractorTestCase(base.TestCase):
    def setUp(self):
        super(DicomMetadataExtractorTestCase, self).setUp()
        self.password = '3achAst5jaWRaCrU'
        self.user = self.model('user').createUser(
            'metadataextractor', self.password, 'Metadata', 'Extractor',
            'metadataextractor@girder.org')
        folders = self.model('folder').childFolders(self.user, 'user',
                                                    user=self.user)
        publicFolders = [folder for folder in folders if folder['public']]
        self.assertIsNotNone(publicFolders)
        self.name = 'sample_dicom.dcm'
        self.patientId = '0522c0001'
        self.item = self.model('item').createItem(self.name, self.user,
                                                  publicFolders[0])
        self.path = os.path.join(ROOT_DIR, 'plugins',
                                 'dicom_metadata_extractor', 'plugin_tests',
                                 'data', self.name)
        upload = self.model('upload').createUpload(
            self.user, self.name, 'item', self.item, os.path.getsize(self.path),
            self.patientId)

        with open(self.path, 'rb') as fd:
            uploadedFile = self.model('upload').handleChunk(upload, fd)

        self.fileId = str(uploadedFile['_id'])
        self.assertHasKeys(uploadedFile,
                           ['assetstoreId', 'created', 'creatorId', 'itemId',
                            'mimeType', 'name', 'size'])
