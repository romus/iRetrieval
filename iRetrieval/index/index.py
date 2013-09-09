# -*- coding: utf-8 -*-


__author__ = 'romus'


from abc import ABCMeta, abstractmethod


class Index():
	""" Класс для создания индекса """

	__metaclass__ = ABCMeta

	@abstractmethod
	def createStatistics(self, dataSourceWorker):
		"""
		Создание статистики по источникам
		(должен вызываться до методов создания индекса)

		:param dataSourceWorker:  объект для работы с источниками (настроки для работы с источниками и тд)
		"""
		pass

	@abstractmethod
	def createTotalStatistics(self):
		"""
		Создание статистики по всем источникам с данными
		(должен вызываться после метода createStatistics, до методов создания индекса)
		"""
		pass

	@abstractmethod
	def createSourceNameIndex(self, customCallback, parseSourceNameCallback, sourceCallback):
		"""
		Создание индекса по именам источников

		:param customCallback:  колбэк для получения данных для работы с источниками
		:param parseSourceNameCallback:  колбэк для обработки имени источника
		:param sourceCallback:  колбэк для работы с источниками
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

	def createStatistics(self, dataSourceWorker):
		pass

	def createTotalStatistics(self):
		pass

	def createSourceNameIndex(self, customCallback, parseSourceNameCallback, sourceCallback):
		pass

	def createSourceDataIndex(self, readSourceDataCallback):
		pass


