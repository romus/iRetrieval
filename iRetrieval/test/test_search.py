# -*- coding: utf-8 -*-


__author__ = 'romus'


import unittest
import datetime

from statistic4text.utils.read_utils import MongoReadUtils

from iRetrieval.errors.errors import ParamError
from iRetrieval.test.connection_configs import *
from iRetrieval.search.search import MongoSearch
from iRetrieval.parser.parser_q import TYPE_Q_LOGIC
from iRetrieval.utils.save_utils import MongoSaveRetrievalUtils
from iRetrieval.utils.read_utils import MongoSearchRetrievalUtils


class TestMongoSearch(unittest.TestCase):

	def testInitException(self):
		self.assertRaises(ParamError, MongoSearch, None)
		self.assertRaises(TypeError, MongoSearch, "string")
		self.assertRaises(TypeError, MongoSearch, MongoReadUtils, HOST, PORT, USR, PWD, DB, FC_N, FC_DN)

	def testSearchNames(self):
		mongoSaveUtils = MongoSaveRetrievalUtils(HOST, PORT, USR, PWD, DB, FC_N, FC_DN, MDN)
		retID = mongoSaveUtils.saveDict("testing name", "utf-8", 1234, {"the": 1, "test": 2},
			"utf-8", datetime.datetime.now())
		mongoSaveUtils.saveFilename(retID, ["testing", "name", "other"], "testing name~")
		retID = mongoSaveUtils.saveDict("some doc", "utf-8", 1234, {"some": 20, "gg": 50},
			"utf-8", datetime.datetime.now())
		mongoSaveUtils.saveFilename(retID, ["some", "doc"], "some doc~")
		retID = mongoSaveUtils.saveDict("some doc 2", "utf-8", 1234, {"some": 20, "gg": 50, "n1": 80},
			"utf-8", datetime.datetime.now())
		mongoSaveUtils.saveFilename(retID, ["some", "doc", "2"], "some doc 2~")

		mongoSearchUtils = MongoSearchRetrievalUtils(HOST, PORT, USR, PWD, DB, FC_N, FC_DN)
		cd = {"result_cn": "rcn"}  # customDict
		cdd = {"is_lazy": False}  # customDictData
		mdID = mongoSaveUtils.getMergeDictID()

		mongoSearch = MongoSearch(mongoSearchUtils)
		self.assertIsNotNone(mongoSearch.searchNames([TYPE_Q_LOGIC, [["doc"], ["doc"]]], cd, cdd, mdID))
		mongoSearch.removeFindObject()
		mongoSaveUtils.deleteMergeDict()
