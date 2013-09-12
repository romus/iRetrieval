# -*- coding: utf-8 -*-


__author__ = 'romus'


import os
import unittest
from statistic4text.errors.errors import DataNotFound
from statistic4text.utils.save_utils import MongoSaveUtils
from statistic4text.utils.source_data_utils import FileBlockSource
from statistic4text.utils.normalization_utils import SimpleNormalization
from iRetrieval.index.index import MongoIndex
from iRetrieval.errors.errors import ParamError
from iRetrieval.utils.datasource_worker_utils import DataSourceWorkerFS
from iRetrieval.utils.read_datasource_utils import FSSourceCustomCallback, ReaderNameFS


class TestMongoIndex(unittest.TestCase):

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
		self.__smN = SimpleNormalization()
		self.__fbs = FileBlockSource()
		self.__scc = FSSourceCustomCallback()
		self.__rFS = ReaderNameFS([firstPath, secondPath])
		self.__fsWorker = DataSourceWorkerFS()

	def tearDown(self):
		try:
			self.__mongoUtils.deleteMergeDict()
		except DataNotFound:
			pass

	def testCreateStatistics(self):
		mongoIndex = MongoIndex(self.__mongoUtils)
		mongoIndex.createStatistics(self.__fsWorker, self.__rFS, self.__fbs, self.__smN, self.__scc)

	def testInitException(self):
		self.assertRaises(ParamError, MongoIndex, None)
		self.assertRaises(TypeError, MongoIndex, "test")

	def testCreateStatisticsException(self):
		mongoIndex = MongoIndex(self.__mongoUtils)
		self.assertRaises(ParamError, mongoIndex.createStatistics, None, self.__rFS, self.__fbs, self.__smN, self.__scc)
		self.assertRaises(TypeError, mongoIndex.createStatistics, "1", self.__rFS, self.__fbs, self.__smN, self.__scc)
