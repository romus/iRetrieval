# -*- coding: utf-8 -*-


__author__ = 'romus'


from abc import ABCMeta, abstractmethod


class Index():
	""" Класс для создания индекса """

	__metaclass__ = ABCMeta

	@abstractmethod
	def createSourceNameIndex(self, sourceNameCallback, parseSourceNameCallback):
		"""
		Создание индекса по именам источников

		:param sourceNameCallback:  колбэк для получения имен источников
		:param parseSourceNameCallback:  колбэк для обработки имени источника
		"""
		pass

	@abstractmethod
	def createSourceDataIndex(self, readSourceDataCallback):
		"""
		Создание индекса по данным источника

		:param readSourceDataCallback:  колбэк для получения данных по источнику
		"""
		pass


class MongoIndex(Index):

	def __init__(self, mongoUtils):
		pass

	def createSourceNameIndex(self, sourceNameCallback, parseSourceNameCallback):
		pass

	def createSourceDataIndex(self, readSourceDataCallback):
		pass


