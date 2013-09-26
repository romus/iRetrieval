# -*- coding: utf-8 -*-


__author__ = 'romus'


import os
from abc import ABCMeta, abstractmethod
from statistic4text.utils.save_utils import MongoSaveUtils
from statistic4text.utils.read_utils import MongoReadUtils
from statistic4text.statistic.statistic import StatisticFactory, MONGO_TYPE
from iRetrieval.errors.errors import ParamError
from iRetrieval.utils.datasource_worker_utils import DataSourceWorker
from iRetrieval.utils.normalization_utils import FileNameNormalization
from iRetrieval.utils.save_utils import ISaveRetrievalUtils, FILENAME_PATH_TYPE, FILENAME_TYPE


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
	def createSourceNameIndex(self, parseSourceNameCallback):
		"""
		Создание индекса по именам источников

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

	def createSourceNameIndex(self, parseSourceNameCallback):
		"""
		Создание индекса по полным именам файлов

		:param parseSourceNameCallback:  колбэк для обработки имен источников
		"""
		if not parseSourceNameCallback:
			raise ParamError("parseSourceNameCallback cannot be the None-object")
		if not isinstance(parseSourceNameCallback, FileNameNormalization):
			raise TypeError("parseSourceNameCallback can be the list FileNameNormalization")

		for file_data in self.__mongoReadUtils.getSubDicts(self.__ms.getMainStatisticID()):
			# получение кортежа '/opt/test dir/file.txt' -> ('/opt/test dir', 'file.txt')
			name_node = os.path.split(file_data['dict_name'])
			try:
				paths = parseSourceNameCallback.normalizeTextWithoutRepetition(name_node[0])
				self.__mongoSaveUtils.saveFilename(file_data['_id'], paths, FILENAME_PATH_TYPE)
				names = parseSourceNameCallback.normalizeTextWithoutRepetition(name_node[1])
				self.__mongoSaveUtils.saveFilename(file_data['_id'], names, FILENAME_TYPE)
			except IndexError as e:
				pass

	def createSourceDataIndex(self, readSourceDataCallback):
		pass
