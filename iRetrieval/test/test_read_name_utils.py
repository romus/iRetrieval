# -*- coding: utf-8 -*-


__author__ = 'romus'


import os
import unittest
from iRetrieval.errors.errors import ParamError
from iRetrieval.utils.read_name_utils import ReaderNameFS


class TestReaderNameFS(unittest.TestCase):

	def setUp(self):
		self.__dirPath = os.path.abspath(os.curdir)

	def testInitException(self):
		self.assertRaises(ParamError, ReaderNameFS, None)
		self.assertRaises(TypeError, ReaderNameFS, "test string param")

	def testGetSourceName(self):
		firstPath = os.path.join(self.__dirPath, "resources/first")
		secondPath = os.path.join(self.__dirPath, "resources/second")
		readerNameFS = ReaderNameFS([firstPath, secondPath])
		for itemFile in readerNameFS.getSourceName():
			self.assertIsNotNone(itemFile, "filename is not to be a None object")

