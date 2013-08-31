# -*- coding: utf-8 -*-


__author__ = 'romus'


import os
import unittest
from statistic4text.utils.source_data_utils import FileSource, FileSourceCustom
from iRetrieval.errors.errors import ParamError
from iRetrieval.utils.read_datasource_utils import ReaderNameFS, FSSourceCustomCallback


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
		fileSource = FileSource()
		fileSourceCustom = FileSourceCustom()
		for itemFile in readerNameFS.getSourceCustom():
			fileSourceCustom.custom = itemFile
			openSource = fileSource.openSource(fileSourceCustom.custom)
			self.assertIsNotNone(fileSource.getName(openSource), "filename is not to be a None object")
			fileSource.closeSource(openSource)

	def testGetSourceNameWithCallback(self):
		firstPath = os.path.join(self.__dirPath, "resources/first")
		secondPath = os.path.join(self.__dirPath, "resources/second")
		readerNameFS = ReaderNameFS([firstPath, secondPath])
		fileSource = FileSource()
		fileSourceCustom = FileSourceCustom()
		sourceCustomCallback = FSSourceCustomCallback()
		for itemFile in readerNameFS.getSourceCustom(sourceCustomCallback):
			fileSourceCustom.custom = itemFile
			openSource = fileSource.openSource(fileSourceCustom.custom)
			self.assertIsNotNone(fileSource.getName(openSource), "filename is not to be a None object")
			fileSource.closeSource(openSource)


class TestFSSourceCustomCallback(unittest.TestCase):

	def testInitException(self):
		self.assertRaises(TypeError, FSSourceCustomCallback, "string, not list")

	def testCheckSourceCustom(self):
		sourceCustomCallback = FSSourceCustomCallback()
		self.assertNotEquals(sourceCustomCallback.checkSourceCustom("test.xxx"), False, "test.xxx is incorrect source")
		self.assertNotEquals(sourceCustomCallback.checkSourceCustom("test.c"), True, "test.xxx is correct source")