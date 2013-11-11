# -*- coding: utf-8 -*-


__author__ = 'romus'


import os
import unittest

from statistic4text.errors.errors import DataNotFound
from statistic4text.utils.read_utils import MongoReadUtils
from statistic4text.utils.source_data_utils import FileBlockSource
from statistic4text.utils.normalization_utils import SimpleNormalization
from statistic4text.statistic.statistic import StatisticFactory, MONGO_TYPE

from iRetrieval.errors.errors import ParamError
from iRetrieval.test.connection_configs import *
from iRetrieval.utils.save_utils import MongoSaveRetrievalUtils
from iRetrieval.utils.normalization_utils import FileNameNormalization
from iRetrieval.utils.datasource_worker_utils import DataSourceWorkerFS
from iRetrieval.utils.read_datasource_utils import FSSourceCustomCallback, ReaderNameFS


class TestDataSourceWorkerFS(unittest.TestCase):

	def setUp(self):
		self.__dirPath = os.path.abspath(os.curdir)
		firstPath = os.path.join(self.__dirPath, "resources/first")
		secondPath = os.path.join(self.__dirPath, "resources/second")
		self.__mongoSaveUtils = MongoSaveRetrievalUtils(HOST, PORT, USR, PWD, DB, FC_N, FC_DN, MDN)
		self.__mongoReadUtils = MongoReadUtils(HOST, PORT, USR, PWD, DB, FC_N, FC_DN)
		self.__simN = SimpleNormalization()
		self.__simNamesN = FileNameNormalization()
		self.__fbs = FileBlockSource()
		self.__ms = StatisticFactory().createStatistic(MONGO_TYPE, self.__mongoSaveUtils)
		self.__scc = FSSourceCustomCallback()
		self.__rnFS = ReaderNameFS([firstPath, secondPath])

	def tearDown(self):
		try:
			self.__mongoSaveUtils.deleteMergeDict()
		except DataNotFound:
			pass

	def testCreateStatistics(self):
		fsWorker = DataSourceWorkerFS()
		fsWorker.createStatistics(self.__ms, self.__rnFS, self.__fbs, self.__simN, self.__scc)

	def testCreateStatisticsException(self):
		fsWorker = DataSourceWorkerFS()
		self.assertRaises(ParamError, fsWorker.createStatistics, None, 2, 3, 4, 5)
		self.assertRaises(TypeError, fsWorker.createStatistics, 1, 2, 3, 4, 5)
		self.assertRaises(ParamError, fsWorker.createStatistics, self.__ms, None, 3, 4, 5)
		self.assertRaises(TypeError, fsWorker.createStatistics, self.__ms, 2, 3, 4, 5)
		self.assertRaises(TypeError, fsWorker.createStatistics, self.__ms, self.__rnFS, self.__fbs, self.__simN, 5)

	def testCreateSourceNameIndex(self):
		fsWorker = DataSourceWorkerFS()
		fsWorker.createStatistics(self.__ms, self.__rnFS, self.__fbs, self.__simN, self.__scc)
		fsWorker.createSourceNameIndex(self.__ms, self.__mongoReadUtils, self.__mongoSaveUtils, self.__simNamesN)

	def testCreateSourceNameIndexException(self):
		fsWorker = DataSourceWorkerFS()
		csn_m = fsWorker.createSourceNameIndex
		self.assertRaises(ParamError, csn_m, None, 2, 3, 4)
		self.assertRaises(TypeError, csn_m, 1, 2, 3, 4)
		self.assertRaises(ParamError, csn_m, self.__ms, None, 3, 4)
		self.assertRaises(TypeError, csn_m, self.__ms, 2, 3, 4)
		self.assertRaises(ParamError, csn_m, self.__ms, self.__mongoReadUtils, None, 4)
		self.assertRaises(TypeError, csn_m, self.__ms, self.__mongoReadUtils, 3, 4)
		self.assertRaises(ParamError, csn_m, self.__ms, self.__mongoReadUtils, self.__mongoSaveUtils, None)
		self.assertRaises(TypeError, csn_m, self.__ms, self.__mongoReadUtils, self.__mongoSaveUtils, 1)
