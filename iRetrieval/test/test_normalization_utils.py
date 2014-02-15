# -*- coding: utf-8 -*-


__author__ = 'romus'

import unittest
from statistic4text.errors.errors import ParamError
from iRetrieval.utils.normalization_utils import FileNameNormalization


class TestFileNameNormalization(unittest.TestCase):

    def setUp(self):
        self.__fileNormalization = FileNameNormalization()

    def testNormalizeText(self):
        words = self.__fileNormalization.normalizeText('/opt/some dir/file.txt')
        for word in words:
            self.assertIsNotNone(word, "empty word")

        words2 = self.__fileNormalization.normalizeText('C:\\some dir\\file.txt')
        for word in words2:
            self.assertIsNotNone(word, "empty word")

    def testNormalizeTextException(self):
        self.assertRaises(ParamError, self.__fileNormalization.normalizeText, None)
        self.assertRaises(ParamError, self.__fileNormalization.normalizeText, '')
