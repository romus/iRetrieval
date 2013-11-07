# -*- coding: utf-8 -*-


__author__ = 'romus'


import unittest
import datetime

from statistic4text.errors.errors import DataNotFound

from iRetrieval.errors.errors import ParamError
from iRetrieval.utils.save_utils import MongoSaveRetrievalUtils


class TestMongoSaveRetrievalUtils(unittest.TestCase):

	def setUp(self):
		h = "192.168.0.80"
		p = 27017
		usr = "statistic"
		pwd = "statistic"
		db = "statistic"
		fc_n = "files"
		fc_dn = "files_data"
		mdn = "test_merge_dict"
		self.__mongoUtils = MongoSaveRetrievalUtils(h, p, usr, pwd, db, fc_n, fc_dn, mdn)

	def tearDown(self):
		try:
			self.__mongoUtils.deleteMergeDict()
		except DataNotFound:
			pass

	def testSaveFilename(self):
		retID = self.__mongoUtils.saveDict("testing name", "utf-8", 1234, {"the": 1, "test": 2},
			"utf-8", datetime.datetime.now())
		self.__mongoUtils.saveFilename(retID, ["one", "test", "run"])

	def testSaveFilenameException(self):
		self.assertRaises(ParamError, self.__mongoUtils.saveFilename, None, 2)
		self.assertRaises(ParamError, self.__mongoUtils.saveFilename, 1, None)
		self.assertRaises(TypeError, self.__mongoUtils.saveFilename, 1, 2)
		self.__mongoUtils.deleteMergeDict()
		self.assertRaises(DataNotFound, self.__mongoUtils.saveFilename, 1, ["one"])
