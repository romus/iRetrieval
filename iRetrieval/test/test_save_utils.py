# -*- coding: utf-8 -*-


__author__ = 'romus'


import unittest

from statistic4text.errors.errors import DataNotFound

from iRetrieval.errors.errors import ParamError
from iRetrieval.utils.save_utils import MongoSaveRetrievalUtils, FILENAME_TYPE


class TestMongoSaveRetrievalUtils(unittest.TestCase):

	def setUp(self):
		h = "192.168.0.80"
		p = 27017
		usr = "statistic"
		pwd = "statistic"
		db = "statistic"
		fc_n = "files"
		fc_dn = "files_data"
		snc = "source_names"
		mdn = "test_merge_dict"
		self.__mongoUtils = MongoSaveRetrievalUtils(h, p, usr, pwd, db, fc_n, fc_dn, snc, mdn)

	def tearDown(self):
		try:
			self.__mongoUtils.deleteMergeDict()
		except DataNotFound:
			pass

	def testSaveFilename(self):
		self.__mongoUtils.saveFilename(1, ["one", "test", "run"], FILENAME_TYPE)

	def testSaveFilenameException(self):
		self.assertRaises(ParamError, self.__mongoUtils.saveFilename, None, 2, 3)
		self.assertRaises(ParamError, self.__mongoUtils.saveFilename, 1, None, 3)
		self.assertRaises(ParamError, self.__mongoUtils.saveFilename, 1, 2, None)
		self.assertRaises(TypeError, self.__mongoUtils.saveFilename, 1, 2, 3)
		self.assertRaises(TypeError, self.__mongoUtils.saveFilename, 1, ["one"], "text type")
		self.assertRaises(TypeError, self.__mongoUtils.saveFilename, 1, ["one"], 3)
		self.__mongoUtils.deleteMergeDict()
		self.assertRaises(DataNotFound, self.__mongoUtils.saveFilename, 1, ["one"], FILENAME_TYPE)
