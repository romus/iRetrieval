# -*- coding: utf-8 -*-


__author__ = 'romus'


import os
import unittest

from statistic4text.errors.errors import DataNotFound
from statistic4text.utils.save_utils import MongoSaveUtils
from statistic4text.utils.read_utils import MongoReadUtils
from statistic4text.utils.normalization_utils import SimpleNormalization

from iRetrieval.index.index import MongoIndex
from iRetrieval.errors.errors import ParamError
from iRetrieval.test.connection_configs import *
from iRetrieval.utils.save_utils import MongoSaveRetrievalUtils
from iRetrieval.utils.normalization_utils import FileNameNormalization
from iRetrieval.utils.datasource_worker_utils import DataSourceWorkerFS
from iRetrieval.utils.read_datasource_utils import FSSourceCustomCallback, ReaderNameFS


class TestMongoIndex(unittest.TestCase):

	def setUp(self):
		self.__dirPath = os.path.abspath(os.curdir)
		firstPath = os.path.join(self.__dirPath, "resources/first")
		secondPath = os.path.join(self.__dirPath, "resources/second")
		self.__mongoUtils = MongoSaveRetrievalUtils(HOST, PORT, USR, PWD, DB, FC_N, FC_DN, MDN)
		self.__mongoUtilsTypeError = MongoSaveUtils(HOST, PORT, USR, PWD, DB, FC_N, FC_DN, MDN)
		self.__mongoReadUtils = MongoReadUtils(HOST, PORT, USR, PWD, DB, FC_N, FC_DN)
		self.__smN = SimpleNormalization()
		self.__scc = FSSourceCustomCallback()
		self.__rFS = ReaderNameFS([firstPath, secondPath])
		self.__fsWorker = DataSourceWorkerFS()

	def tearDown(self):
		self.clearCreatedData(self.__mongoUtils)
		self.clearCreatedData(self.__mongoUtilsTypeError)

	def testCreateStatistics(self):
		mongoIndex = MongoIndex(self.__mongoUtils, self.__mongoReadUtils)
		mongoIndex.createStatistics(self.__fsWorker, self.__rFS, self.__smN, self.__scc)

	def testInitException(self):
		self.assertRaises(ParamError, MongoIndex, None, self.__mongoReadUtils)
		self.assertRaises(TypeError, MongoIndex, "test", self.__mongoReadUtils)
		self.assertRaises(TypeError, MongoIndex, self.__mongoUtilsTypeError, self.__mongoReadUtils)
		self.assertRaises(ParamError, MongoIndex, self.__mongoUtils, None)
		self.assertRaises(TypeError, MongoIndex, self.__mongoUtils, "test")

	def testCreateStatisticsException(self):
		mongoIndex = MongoIndex(self.__mongoUtils, self.__mongoReadUtils)
		self.assertRaises(ParamError, mongoIndex.createStatistics, None, self.__rFS, self.__smN, self.__scc)
		self.assertRaises(TypeError, mongoIndex.createStatistics, "1", self.__rFS, self.__smN, self.__scc)

	def testCreateSourceNameIndex(self):
		mongoIndex = MongoIndex(self.__mongoUtils, self.__mongoReadUtils)
		simNamesN = FileNameNormalization()
		mongoIndex.createStatistics(self.__fsWorker, self.__rFS, self.__smN, self.__scc)
		mongoIndex.createSourceNameIndex(self.__fsWorker, simNamesN)

	def testCreateSourceNameIndexException(self):
		mongoIndex = MongoIndex(self.__mongoUtils, self.__mongoReadUtils)
		self.assertRaises(ParamError, mongoIndex.createSourceNameIndex, None, 2)
		self.assertRaises(TypeError, mongoIndex.createSourceNameIndex, 1, 2)
		self.assertRaises(ParamError, mongoIndex.createSourceNameIndex, self.__fsWorker, None)
		self.assertRaises(TypeError, mongoIndex.createSourceNameIndex, self.__fsWorker, 2)

	def clearCreatedData(self, utils):
		try:
			utils.deleteMergeDict()
		except DataNotFound:
			pass
