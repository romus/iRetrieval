# -*- coding: utf-8 -*-


__author__ = 'romus'


import unittest
import datetime

from statistic4text.errors.errors import DataNotFound

from iRetrieval.errors.errors import ParamError
from iRetrieval.test.connection_configs import *
from iRetrieval.parser.parser_q import TYPE_Q_LOGIC, TYPE_Q_EXACT
from iRetrieval.utils.save_utils import MongoSaveRetrievalUtils
from iRetrieval.utils.read_utils import MongoSearchRetrievalUtils


class TestMongoSearchRetrievalUtils(unittest.TestCase):

	def setUp(self):
		self.mongoSaveUtils = MongoSaveRetrievalUtils(HOST, PORT, USR, PWD, DB, FC_N, FC_DN, MDN)
		retID = self.mongoSaveUtils.saveDict("testing name", "utf-8", 1234, {"the": 1, "test": 2},
			"utf-8", datetime.datetime.now())
		self.mongoSaveUtils.saveFilename(retID, ["testing", "name", "other"], "testing name~")
		retID = self.mongoSaveUtils.saveDict("some doc", "utf-8", 1234, {"some": 20, "gg": 50},
			"utf-8", datetime.datetime.now())
		self.mongoSaveUtils.saveFilename(retID, ["some", "doc"], "some doc~")
		retID = self.mongoSaveUtils.saveDict("some doc 2", "utf-8", 1234, {"some": 20, "gg": 50, "n1": 80},
			"utf-8", datetime.datetime.now())
		self.mongoSaveUtils.saveFilename(retID, ["some", "doc", "2"], "some doc 2~")

	def tearDown(self):
		try:
			self.mongoSaveUtils.deleteMergeDict()
		except DataNotFound:
			pass

	def testSearchFilename(self):
		mongoSearch = MongoSearchRetrievalUtils(HOST, PORT, USR, PWD, DB, FC_N, FC_DN)
		customDict = {"result_cn": "rcn"}
		mdID = self.mongoSaveUtils.getMergeDictID()
		findObject = mongoSearch.searchFilename([TYPE_Q_LOGIC, [["doc"], ["doc"]]], customDict, mdID)
		self.assertIsNotNone(findObject, "findObject == None")
		mongoSearch.removeSearchData(findObject)

	def testSearchFilenameException(self):
		mongoSearch = MongoSearchRetrievalUtils(HOST, PORT, USR, PWD, DB, FC_N, FC_DN)
		customDict = {"result_cn": "rcn"}
		mdID = self.mongoSaveUtils.getMergeDictID()
		self.assertRaises(ParamError, mongoSearch.searchFilename, None, customDict, mdID)
		self.assertRaises(ParamError, mongoSearch.searchFilename, [TYPE_Q_LOGIC, [["doc"], ["doc"]]], None, mdID)
		self.assertRaises(ParamError, mongoSearch.searchFilename, [TYPE_Q_LOGIC, [["doc"], ["doc"]]], customDict, None)
		self.assertRaises(TypeError, mongoSearch.searchFilename, "string", customDict, mdID)
		self.assertRaises(TypeError, mongoSearch.searchFilename, [TYPE_Q_LOGIC, [["doc"], ["doc"]]], "string", mdID)
		self.assertRaises(KeyError, mongoSearch.searchFilename, [TYPE_Q_LOGIC, [["doc"], ["doc"]]], {"aa": 10}, mdID)

	def testGetSearchData(self):
		mongoSearch = MongoSearchRetrievalUtils(HOST, PORT, USR, PWD, DB, FC_N, FC_DN)
		customDict = {"result_cn": "rcn"}
		customDictData = {"is_lazy": False}
		mdID = self.mongoSaveUtils.getMergeDictID()

		# логический запрос
		findObject = mongoSearch.searchFilename([TYPE_Q_LOGIC, [["doc"], ["doc"]]], customDict, mdID)
		result = mongoSearch.getSearchData(findObject, customDictData)
		for doc in result:
			self.assertIsNotNone(doc, "map-reduce doc == None")
		customDictData["is_lazy"] = True
		result = mongoSearch.getSearchData(findObject, customDictData)
		for doc in result:
			self.assertIsNotNone(doc, "map-reduce doc == None")
			self.assertEqual(int(doc["value"]["count"]), 2, "count != 2")

		# запрос точного совпадения
		findObject = mongoSearch.searchFilename([TYPE_Q_EXACT, "some doc~"], customDict, mdID)
		result = mongoSearch.getSearchData(findObject, customDictData)
		for doc in result:
			self.assertIsNotNone(doc, "map-reduce doc == None")
		customDictData["is_lazy"] = True
		result = mongoSearch.getSearchData(findObject, customDictData)
		for doc in result:
			self.assertIsNotNone(doc, "map-reduce doc == None")

		mongoSearch.removeSearchData(findObject)

	def testGetSearchDataException(self):
		mongoSearch = MongoSearchRetrievalUtils(HOST, PORT, USR, PWD, DB, FC_N, FC_DN)
		customDict = {"result_cn": "rcn"}
		customDictData = {"is_lazy": False}
		mdID = self.mongoSaveUtils.getMergeDictID()
		findObject = mongoSearch.searchFilename([TYPE_Q_LOGIC, [["doc"], ["doc"]]], customDict, mdID)

		self.assertRaises(ParamError, mongoSearch.getSearchData, None, customDictData)
		self.assertRaises(ParamError, mongoSearch.getSearchData, findObject, None)
		self.assertRaises(TypeError, mongoSearch.getSearchData, "string", customDictData)
		self.assertRaises(TypeError, mongoSearch.getSearchData, findObject, "string")
		self.assertRaises(KeyError, mongoSearch.getSearchData, findObject, {"bb": 40})

		mongoSearch.removeSearchData(findObject)
