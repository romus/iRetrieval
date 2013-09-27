# -*- coding: utf-8 -*-


__author__ = 'romus'


from abc import ABCMeta, abstractmethod
from statistic4text.utils.save_utils import MongoSaveUtils
from statistic4text.utils.read_utils import MongoReadUtils
from statistic4text.statistic.statistic import StatisticFactory, MONGO_TYPE
from iRetrieval.errors.errors import ParamError
from iRetrieval.utils.datasource_worker_utils import DataSourceWorker
from iRetrieval.utils.save_utils import ISaveRetrievalUtils


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
	def createSourceNameIndex(self, dataSourceWorker, parseCallback):
		"""
		Создание индекса по именам источников

		:param dataSourceWorker:  объект для работы с источниками (настроки для работы с источниками и тд)
		:param parseCallback:  колбэк для обработки имени источника
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

	def __init__(self, mongoSaveUtils, mongoReadUtils):
		"""
		инициализация

		:param mongoSaveUtils:  параметры для записи данных в mongodb
		:param mongoReadUtils:  параметры для чтения данных из mongodb
		"""
		if not mongoSaveUtils:
			raise ParamError("mongoUtils cannot be the None-object")
		if not isinstance(mongoSaveUtils, MongoSaveUtils):
			raise TypeError("mongoUtils can be the list MongoSaveUtils")
		if not ISaveRetrievalUtils.providedBy(mongoSaveUtils):
			raise TypeError("mongoUtils is not provided by ISaveRetrievalUtils")

		if not mongoReadUtils:
			raise ParamError("mongoReadUtils cannot be the None-object")
		if not isinstance(mongoReadUtils, MongoReadUtils):
			raise TypeError("mongoReadUtils can be the list MongoReadUtils")

		self.__mongoSaveUtils = mongoSaveUtils
		self.__mongoReadUtils = mongoReadUtils
		self.__ms = StatisticFactory().createStatistic(MONGO_TYPE, self.__mongoSaveUtils)

	def createStatistics(self, dataSourceWorker, readerSourceData, source, normalization, sourceCusCallback=None):
		if not dataSourceWorker:
			raise ParamError("dataSourceWorker cannot be the None-object")
		if not isinstance(dataSourceWorker, DataSourceWorker):
			raise TypeError("mongoUtils can be the list MongoSaveUtils")

		dataSourceWorker.createStatistics(self.__ms, readerSourceData, source, normalization, sourceCusCallback)

	def createTotalStatistics(self):
		self.__ms.makeTotalStatistic()

	def createSourceNameIndex(self, dataSourceWorker, parseCallback):
		"""
		Создание индекса по полным именам файлов

		:param dataSourceWorker:  объект для работы с источниками (настроки для работы с источниками и тд)
		:param parseCallback:  колбэк для обработки имен источников
		"""
		if not dataSourceWorker:
			raise ParamError("dataSourceWorker cannot be the None-object")
		if not isinstance(dataSourceWorker, DataSourceWorker):
			raise TypeError("mongoUtils can be the list MongoSaveUtils")

		dataSourceWorker.createSourceNameIndex(self.__ms, self.__mongoReadUtils, self.__mongoSaveUtils, parseCallback)

	def createSourceDataIndex(self, readSourceDataCallback):
		pass
