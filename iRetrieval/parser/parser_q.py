# -*- coding: utf-8 -*-


__author__ = 'romus'


from abc import ABCMeta, abstractmethod

from statistic4text.utils.normalization_utils import Normalization

from iRetrieval.errors.errors import ParamError


TYPE_Q_LOGIC = 0  # логический поисковый запрос
TYPE_Q_EXACT = 1  # точный поисковый запрос
TYPE_Q_IMPRECISE = 2  # неточный поисковый запрос
TYPE_Q_FULL = 3  # полнотестовый поисковый запрос


class ParserQ():

	__metaclass__ = ABCMeta

	@abstractmethod
	def parseQ(self, q, propertyQ, normalizationCallback):
		"""
		Обработка поискового запроса

		:param q:  поисковый запрос
		:param propertyQ:  параметры запроса
		:param normalizationCallback:  колбэк для нормализации текста
		:return:  тип запроса, обработанный запрос
		"""
		return None

	@abstractmethod
	def parseSourceNameQ(self, q, propertyQ):
		"""
		Обработка поискового запроса по именам источников

		:param q:  поисковый запрос
		:param propertyQ:  параметры запроса
		:return:  тип запроса, слова поискового запроса
		"""
		return None


class SimpleParserQ(ParserQ):

	exact_match_symbol = "\""
	logic_and_symbol = "&"
	logic_or_symbol = "|"

	def parseSourceNameQ(self, q, propertyQ):
		"""
		Обработка поискового завпроса по именам источников

		Получение логического выражения из запроса или запроса по точному совпадению.
		В запросе могут быть специальные логические символы:
		& - логическое "И"; | - логическое "ИЛИ", "это запрос по точному совпадению"
		:param q:  поисковый запрос
		:param propertyQ:  параметры запроса (кодировка, клиент)
		:return: список формата -[type, [[слово1, слово2], [слово3, ...], ...] ],
		где словоX - слова;
		внутренние списки - это слова, связанные логическим "И",
		внутренние списки связанны логическим "ИЛИ".
		type - тип поиска: 0 - логический, 1 - точный, 2 - неточный.
		Для запроса по точному совпадению или нелогическому запросу
		вернется список формата [type, ["q"]].
		"""
		#  TODO учёт кодировки запроса - не сделан
		if not q:
			raise ParamError("Empty query")

		logic_exp = [TYPE_Q_LOGIC]

		# если поступил запрос на точное совпадение
		len_query = len(q)
		count_match_symbol = q.count(self.exact_match_symbol, 0, len_query)
		if count_match_symbol == 2 and q[0] == self.exact_match_symbol and q[-1] == self.exact_match_symbol:
			logic_exp[0] = TYPE_Q_EXACT
			logic_exp.append([q[1: len_query - 1]])
			return logic_exp

		add_node = []
		last_symbol = 0
		isLogic = False
		for x in range(0, len_query):
			if q[x] == self.logic_or_symbol:
				self._addNode(add_node, last_symbol, x, q, "parse error logic 'or'. Query = " + q)
				logic_exp.append(add_node)
				add_node = []
				last_symbol = x + 1
				isLogic = True
			elif q[x] == self.logic_and_symbol:
				self._addNode(add_node, last_symbol, x, q, "parse error logic 'and'. Query = " + q)
				last_symbol = x + 1
				isLogic = True

		last_word = ' '.join(q[last_symbol: len_query].split())
		if last_word:
			add_node.append(last_word)
		else:
			if q[last_symbol - 1] == self.logic_or_symbol or q[last_symbol - 1] == self.logic_and_symbol:
				raise Exception("parse error. Query = " + q)

		if add_node:
			logic_exp.append(add_node)

		if not isLogic:
			logic_exp[0] = TYPE_Q_IMPRECISE

		return logic_exp

	def parseQ(self, q, propertyQ, normalizationCallback):
		"""
		Обработка поискового запроса по именам источников

		:param q:  поисковый запрос
		:param propertyQ:  параметры запроса
		:param normalizationCallback:  колбэк для нормализации текста
		:return:  тип запроса, слова поискового запроса без повторения
		"""
		# TODO проверить кодировки
		if not q:
			raise ParamError("Empty query")

		if not normalizationCallback:
			raise ParamError("normalizationCallback cannot be the None-object")
		if not isinstance(normalizationCallback, Normalization):
			raise TypeError("normalizationCallback can be the list Normalization")

		return [TYPE_Q_FULL, normalizationCallback.normalizeTextWithoutRepetition(q)]


	def _addNode(self, listNode, last, cur, query, exceptionMessage):
		"""Добавление слагаемого"""
		temp_word = ' '.join(query[last: cur].split())
		if not temp_word:
			raise Exception(exceptionMessage)
		listNode.append(temp_word)
