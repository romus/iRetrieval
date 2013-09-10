# -*- coding: utf-8 -*-


__author__ = 'romus'


import os
import unittest
from statistic4text.errors.errors import DataNotFound
from statistic4text.utils.save_utils import MongoSaveUtils
from statistic4text.utils.source_data_utils import FileBlockSource
from statistic4text.utils.normalization_utils import SimpleNormalization
from statistic4text.statistic.statistic import StatisticFactory, MONGO_TYPE
from iRetrieval.errors.errors import ParamError
from iRetrieval.utils.datasource_worker_utils import DataSourceWorkerFS
from iRetrieval.utils.read_datasource_utils import FSSourceCustomCallback, ReaderNameFS


class TestDataSourceWorkerFS(unittest.TestCase):
	def setUp(self):
		h = "192.168.0.80"
		p = 27017
		usr = "statistic"
		pwd = "statistic"
		db = "statistic"
		fc_n = "files"
		fc_dn = "files_data"
		mdn = "test_merge_dict"

		self.__dirPath = os.path.abspath(os.curdir)
		firstPath = os.path.join(self.__dirPath, "resources/first")
		secondPath = os.path.join(self.__dirPath, "resources/second")
		self.__mongoUtils = MongoSaveUtils(h, p, usr, pwd, db, fc_n, fc_dn, mdn)
		self.__simN = SimpleNormalization()
		self.__fbs = FileBlockSource()
		self.__ms = StatisticFactory().createStatistic(MONGO_TYPE, self.__mongoUtils)
		self.__scc = FSSourceCustomCallback()
		self.__rnFS = ReaderNameFS([firstPath, secondPath])

	def tearDown(self):
		try:
			self.__mongoUtils.deleteMergeDict()
		except DataNotFound:
			pass

	def testCreateStatistics(self):
		fsWorker = DataSourceWorkerFS()
		fsWorker.createStatistics(self.__ms, self.__rnFS, self.__fbs, self.__simN, self.__scc)

	def testCreateStatisticsException(self):
		fsWorker = DataSourceWorkerFS()
		self.assertRaises(ParamError, fsWorker.createStatistics, None, 2, 3, 4, 5)
		self.assertRaises(ParamError, fsWorker.createStatistics, 1, None, 3, 4, 5)
		self.assertRaises(TypeError, fsWorker.createStatistics, 1, 2, 3, 4, 5)
		self.assertRaises(TypeError, fsWorker.createStatistics, self.__ms, 2, 3, 4, 5)
		self.assertRaises(TypeError, fsWorker.createStatistics, self.__ms, self.__rnFS, self.__fbs, self.__simN, 5)
