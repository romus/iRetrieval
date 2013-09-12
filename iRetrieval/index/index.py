# -*- coding: utf-8 -*-


__author__ = 'romus'


from abc import ABCMeta, abstractmethod
from statistic4text.utils.save_utils import MongoSaveUtils
from statistic4text.statistic.statistic import StatisticFactory, MONGO_TYPE
from iRetrieval.errors.errors import ParamError
from iRetrieval.utils.datasource_worker_utils import DataSourceWorker


class Index():
	""" Класс для создания индекса """

	__metaclass__ = ABCMeta

	@abstractmethod
	def createStatistics(self, dataSourceWorker, readerSourceData, source, normalization, sourceCustomCallback=None):
		"""
		Создание статистики по источникам
		(должен вызываться до методов создания индекса)

		:param dataSourceWorker:  объект для работы с источниками (настроки для работы с источниками и тд)
		:param readerSourceData:  объект для получения настроект для работы с источниками
		:param source:  объект для чтения данных из источника
		:param normalization:  объект для нормализации данных
		:param sourceCustomCallback:  колбэк для объекта получения настроек
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
		"""
		инициализация

		:param mongoUtils:  параметры для работы с mongodb
		"""
		if not mongoUtils:
			raise ParamError("mongoUtils cannot be the None-object")
		if not isinstance(mongoUtils, MongoSaveUtils):
			raise TypeError("mongoUtils can be the list MongoSaveUtils")

		self.__ms = StatisticFactory().createStatistic(MONGO_TYPE, mongoUtils)

	def createStatistics(self, dataSourceWorker, readerSourceData, source, normalization, sourceCusCallback=None):
		if not dataSourceWorker:
			raise ParamError("dataSourceWorker cannot be the None-object")
		if not isinstance(dataSourceWorker, DataSourceWorker):
			raise TypeError("mongoUtils can be the list MongoSaveUtils")

		dataSourceWorker.createStatistics(self.__ms, readerSourceData, source, normalization, sourceCusCallback)

	def createTotalStatistics(self):
		pass

	def createSourceNameIndex(self, customCallback, parseSourceNameCallback, sourceCallback):
		pass

	def createSourceDataIndex(self, readSourceDataCallback):
		pass
