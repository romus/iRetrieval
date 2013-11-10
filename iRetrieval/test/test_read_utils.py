# -*- coding: utf-8 -*-


__author__ = 'romus'


import unittest
import datetime

from statistic4text.errors.errors import DataNotFound

from iRetrieval.errors.errors import ParamError
from iRetrieval.parser.parser_q import TYPE_Q_LOGIC
from iRetrieval.utils.save_utils import MongoSaveRetrievalUtils
from iRetrieval.utils.read_utils import MongoSearchRetrievalUtils


class TestMongoSearchRetrievalUtils(unittest.TestCase):

	def setUp(self):
		self.h = "192.168.0.80"
		self.p = 27017
		self.usr = "statistic"
		self.pwd = "statistic"
		self.db = "statistic"
		self.fc_n = "files"
		self.fc_dn = "files_data"
		self.mdn = "test_merge_dict"
		self.mongoSaveUtils = MongoSaveRetrievalUtils(self.h, self.p, self.usr, self.pwd,
												  self.db, self.fc_n, self.fc_dn, self.mdn)
		retID = self.mongoSaveUtils.saveDict("testing name", "utf-8", 1234, {"the": 1, "test": 2},
			"utf-8", datetime.datetime.now())
		self.mongoSaveUtils.saveFilename(retID, ["testing", "name", "other"])
		retID = self.mongoSaveUtils.saveDict("some doc", "utf-8", 1234, {"some": 20, "gg": 50},
			"utf-8", datetime.datetime.now())
		self.mongoSaveUtils.saveFilename(retID, ["some", "doc"])
		retID = self.mongoSaveUtils.saveDict("some doc 2", "utf-8", 1234, {"some": 20, "gg": 50, "n1": 80},
			"utf-8", datetime.datetime.now())
		self.mongoSaveUtils.saveFilename(retID, ["some", "doc", "2"])

	def tearDown(self):
		try:
			self.mongoSaveUtils.deleteMergeDict()
		except DataNotFound:
			pass

	def testSearchFilename(self):
		mongoSearch = MongoSearchRetrievalUtils(self.h, self.p, self.usr, self.pwd, self.db,
												self.fc_n, self.fc_dn)
		customDict = {"result_cn": "rcn"}
		findObject = mongoSearch.searchFilename([TYPE_Q_LOGIC, [["doc"], ["doc"]]], customDict)
		self.assertIsNotNone(findObject, "findObject == None")
		mongoSearch.removeSearchData(findObject)

	def testSearchFilenameException(self):
		mongoSearch = MongoSearchRetrievalUtils(self.h, self.p, self.usr, self.pwd, self.db,
												self.fc_n, self.fc_dn)
		customDict = {"result_cn": "rcn"}
		self.assertRaises(ParamError, mongoSearch.searchFilename, None, customDict)
		self.assertRaises(ParamError, mongoSearch.searchFilename, [TYPE_Q_LOGIC, [["doc"], ["doc"]]], None)
		self.assertRaises(TypeError, mongoSearch.searchFilename, "string", customDict)
		self.assertRaises(TypeError, mongoSearch.searchFilename, [TYPE_Q_LOGIC, [["doc"], ["doc"]]], "string")
		self.assertRaises(KeyError, mongoSearch.searchFilename, [TYPE_Q_LOGIC, [["doc"], ["doc"]]], {"aa": 10})

	def testGetSearchData(self):
		mongoSearch = MongoSearchRetrievalUtils(self.h, self.p, self.usr, self.pwd, self.db,
												self.fc_n, self.fc_dn)
		customDict = {"result_cn": "rcn"}
		customDictData = {"is_lazy": False}
		findObject = mongoSearch.searchFilename([TYPE_Q_LOGIC, [["doc"], ["doc"]]], customDict)

		result = mongoSearch.getSearchData(findObject, customDictData)
		for doc in result:
			self.assertIsNotNone(doc, "map-reduce doc == None")
		customDictData["is_lazy"] = True
		result = mongoSearch.getSearchData(findObject, customDictData)
		for doc in result:
			self.assertIsNotNone(doc, "map-reduce doc == None")

		mongoSearch.removeSearchData(findObject)

	def testGetSearchDataException(self):
		mongoSearch = MongoSearchRetrievalUtils(self.h, self.p, self.usr, self.pwd, self.db,
												self.fc_n, self.fc_dn)
		customDict = {"result_cn": "rcn"}
		customDictData = {"is_lazy": False}
		findObject = mongoSearch.searchFilename([TYPE_Q_LOGIC, [["doc"], ["doc"]]], customDict)

		self.assertRaises(ParamError, mongoSearch.getSearchData, None, customDictData)
		self.assertRaises(ParamError, mongoSearch.getSearchData, findObject, None)
		self.assertRaises(TypeError, mongoSearch.getSearchData, "string", customDictData)
		self.assertRaises(TypeError, mongoSearch.getSearchData, findObject, "string")
		self.assertRaises(KeyError, mongoSearch.getSearchData, findObject, {"bb": 40})

		mongoSearch.removeSearchData(findObject)
