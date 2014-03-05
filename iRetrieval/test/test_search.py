# -*- coding: utf-8 -*-


__author__ = 'romus'


import unittest
import datetime

from statistic4text.errors.errors import DataNotFound
from statistic4text.utils.read_utils import MongoReadUtils

from iRetrieval.errors.errors import ParamError
from iRetrieval.test.connection_configs import *
from iRetrieval.search.search import MongoSearch
from iRetrieval.parser.parser_q import TYPE_Q_LOGIC
from iRetrieval.utils.save_utils import MongoSaveRetrievalUtils
from iRetrieval.utils.read_utils import MongoSearchRetrievalUtils


class TestMongoSearch(unittest.TestCase):

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

    def testInitException(self):
        self.assertRaises(ParamError, MongoSearch, None)
        self.assertRaises(TypeError, MongoSearch, "string")
        self.assertRaises(TypeError, MongoSearch, MongoReadUtils, HOST, PORT, USR, PWD, DB, FC_N, FC_DN)

    def testSearchNames(self):
        mongoSearchUtils = MongoSearchRetrievalUtils(HOST, PORT, USR, PWD, DB, FC_N, FC_DN)
        cd = {"result_cn": "rcn"}  # customDict
        cdd = {"is_lazy": False}  # customDictData
        mdID = self.mongoSaveUtils.getMergeDictID()

        mongoSearch = MongoSearch(mongoSearchUtils)
        self.assertIsNotNone(mongoSearch.searchNames([TYPE_Q_LOGIC, [["doc"], ["doc"]]], cd, cdd, mdID))
        mongoSearch.removeFindObject()

    def testSearchData(self):
        mongoSearchUtils = MongoSearchRetrievalUtils(HOST, PORT, USR, PWD, DB, FC_N, FC_DN)
        cd = {"result_cn": "rcd"}  # customDict
        cdd = {"is_lazy": False}  # customDictData
        mdID = self.mongoSaveUtils.getMergeDictID()

        mongoSearch = MongoSearch(mongoSearchUtils)
        self.assertIsNotNone(mongoSearch.searchData([None, ["the"]], cd, cdd, mdID))
        mongoSearch.removeFindObject()
