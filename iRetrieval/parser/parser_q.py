# -*- coding: utf-8 -*-


__author__ = 'romus'


from abc import ABCMeta, abstractmethod


class ParserQ():

	__metaclass__ = ABCMeta

	@abstractmethod
	def parseQ(self, q, propertyQ):
		"""
		Обработка поискового запроса

		:param q:  поисковый запрос
		:param propertyQ:  параметры запроса
		:return:  тип запроса, обработанный запрос
		"""
		return None