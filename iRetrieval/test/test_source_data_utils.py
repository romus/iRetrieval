# -*- coding: utf-8 -*-


__author__ = 'romus'

import os
import unittest

from iRetrieval.utils.source_data_utils import OfficeFileSource


class TestOfficeFileSource(unittest.TestCase):

    def setUp(self):
        self.__of_file_source = OfficeFileSource()
        self.__dir_path = os.path.abspath(os.curdir)

    def testGetSource(self):
        file_path = os.path.join(self.__dir_path, "resources/office.docx")
        source = self.__of_file_source.openSource(file_path)
        self.assertIsNotNone(source, "not open source")
        self.__of_file_source.closeSource(source)

    def testGetSourceThrowIOError(self):
        file_path = os.path.join(self.__dir_path, "resources/not_exist_file")
        self.assertRaises(IOError, self.__of_file_source.openSource, file_path)

    def testRead(self):
        file_path = os.path.join(self.__dir_path, "resources/office.docx")
        source = self.__of_file_source.openSource(file_path)
        for line in self.__of_file_source.read(source):
            self.assertIsNotNone(line)
        self.__of_file_source.closeSource(source)

    def testGetName(self):
        file_path = os.path.join(self.__dir_path, "resources/office.docx")
        source = self.__of_file_source.openSource(file_path)
        self.assertIsNotNone(self.__of_file_source.getName(source))
        self.__of_file_source.closeSource(source)

    def testGetSourceSize(self):
        file_path = os.path.join(self.__dir_path, "resources/office.docx")
        source = self.__of_file_source.openSource(file_path)
        self.assertIsNotNone(self.__of_file_source.getSourceSize(source))
        self.__of_file_source.closeSource(source)

    def testGetSourceDateCreated(self):
        file_path = os.path.join(self.__dir_path, "resources/office.docx")
        source = self.__of_file_source.openSource(file_path)
        self.assertIsNotNone(self.__of_file_source.getSourceDateCreated(source))
        self.__of_file_source.closeSource(source)

    def testGetSourceDateModified(self):
        file_path = os.path.join(self.__dir_path, "resources/office.docx")
        source = self.__of_file_source.openSource(file_path)
        self.assertIsNotNone(self.__of_file_source.getSourceDateModified(source))
        self.__of_file_source.closeSource(source)
