# -*- coding: utf-8 -*-


__author__ = 'romus'

import unittest
import datetime

from statistic4text.errors.errors import DataNotFound

from iRetrieval.errors.errors import ParamError
from iRetrieval.test.connection_configs import *
from iRetrieval.utils.save_utils import MongoSaveRetrievalUtils


class TestMongoSaveRetrievalUtils(unittest.TestCase):

    def setUp(self):
        self.__mongoUtils = MongoSaveRetrievalUtils(HOST, PORT, USR, PWD, DB, FC_N, FC_DN, MDN)

    def tearDown(self):
        try:
            self.__mongoUtils.deleteMergeDict()
        except DataNotFound:
            pass

    def testSaveFilename(self):
        retID = self.__mongoUtils.saveDict("testing name", "utf-8", 1234, {"the": 1, "test": 2},
                                           "utf-8", datetime.datetime.now())
        self.__mongoUtils.saveFilename(retID, ["one", "test", "run"], "testing name")

    def testSaveFilenameException(self):
        self.assertRaises(ParamError, self.__mongoUtils.saveFilename, None, 2, 3)
        self.assertRaises(ParamError, self.__mongoUtils.saveFilename, 1, None, 3)
        self.assertRaises(ParamError, self.__mongoUtils.saveFilename, 1, 2, None)
        self.assertRaises(TypeError, self.__mongoUtils.saveFilename, 1, 2, 3)
        self.__mongoUtils.deleteMergeDict()
        self.assertRaises(DataNotFound, self.__mongoUtils.saveFilename, 1, ["one"], "one")
