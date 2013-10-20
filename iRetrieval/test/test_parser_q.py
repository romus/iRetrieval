# -*- coding: utf-8 -*-


__author__ = 'romus'


import unittest

from statistic4text.utils.normalization_utils import SimpleNormalization

from iRetrieval.errors.errors import ParamError
from iRetrieval.parser.parser_q import SimpleParserQ, TYPE_Q_LOGIC, TYPE_Q_EXACT, TYPE_Q_IMPRECISE, TYPE_Q_FULL


#  TODO добавить объект - параметры поискового запроса
class TestSimpleParserQ(unittest.TestCase):

	def setUp(self):
		self.spq = SimpleParserQ()

	def testParseSourceNameQ(self):
		self.assertEqual(self.spq.parseSourceNameQ("simple | logic & q", None)[0], TYPE_Q_LOGIC)
		self.assertEqual(self.spq.parseSourceNameQ('"a simple q"', None)[0], TYPE_Q_EXACT)
		self.assertEqual(self.spq.parseSourceNameQ("a simple q", None)[0], TYPE_Q_IMPRECISE)

	def testParseSourceNameQException(self):
		self.assertRaises(ParamError, self.spq.parseSourceNameQ, None, None)
		self.assertRaises(Exception, self.spq.parseSourceNameQ, "simple | | q", None)
		self.assertRaises(Exception, self.spq.parseSourceNameQ, "simple && q", None)
		self.assertRaises(Exception, self.spq.parseSourceNameQ, "simple & q |", None)

	def testParseQ(self):
		smN = SimpleNormalization()
		parseList = self.spq.parseQ("testing q q q q testing", None, smN)
		self.assertEqual(parseList[0], TYPE_Q_FULL)
		self.assertListEqual(parseList[1], ["test", "q"])
