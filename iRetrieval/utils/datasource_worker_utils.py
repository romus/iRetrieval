# -*- coding: utf-8 -*-


__author__ = 'romus'


import os
from abc import ABCMeta, abstractmethod

from statistic4text.statistic.statistic import Statistic
from statistic4text.utils.save_utils import MongoSaveUtils
from statistic4text.utils.read_utils import MongoReadUtils
from statistic4text.utils.source_data_utils import FileSourceCustom

from iRetrieval.errors.errors import ParamError
from iRetrieval.utils.save_utils import ISaveRetrievalUtils
from iRetrieval.utils.normalization_utils import FileNameNormalization
from iRetrieval.utils.save_utils import FILENAME_PATH_TYPE, FILENAME_TYPE
from iRetrieval.utils.read_datasource_utils import ReaderSourceData, SourceCustomCallback


class DataSourceWorker():
	""" Класс для создания статистики по источникам и данным из этих источников """

	__metaclass__ = ABCMeta

	@abstractmethod
	def createStatistics(self, statisticObject, readerSourceData, normalization, source, sourceCustomCallback=None):
		"""
		Создание статистики по объектам и данным из файловой системы

		:param statisticObject:  объект для создания статистики
		:param readerSourceData:  объект для получения настроект для работы с источниками
		:param source:  объект для чтения данных из источника
		:param normalization:  объект для нормализации данных
		:param sourceCustomCallback:  колбэк для объекта получения настроек
		"""
		pass

	@abstractmethod
	def createSourceNameIndex(self, statisticObject, readSourceUtils, saveSourceUtils, parseSourceNameCallback):
		"""
		Создание индекса по названим источников

		:param statisticObject:  объект для создания статистики
		:param readSourceUtils:  объект для чтения данных статистики
		:param saveSourceUtils:  объект для сохранения индекса по статистике
		:param parseSourceNameCallback:  колбэк для обработки имен источников
		"""
		pass


class DataSourceWorkerFS(DataSourceWorker):
	""" Класс для создания статистики по файлам (работа с файловой системой) """

	def __init__(self):
		pass

	def createStatistics(self, statisticObject, readerSourceData, source, normalization, sourceCustomCallback=None):
		"""

		:param statisticObject:  объект для создания статистики
		:param readerSourceData:  объект для получения полных путей к файлам
		:param source:  объект для чтения данных из файла
		:param normalization:  объект для нормализации данных
		:param sourceCustomCallback:  колбэк для объекта получения настроек (верификация путей)
		"""
		if not statisticObject:
			raise ParamError("statisticObject cannot be the None-object")
		if not isinstance(statisticObject, Statistic):
			raise TypeError("statisticObject can be the list Statistic")

		if not readerSourceData:
			raise ParamError("readerSourceData cannot be the None-object")
		if not isinstance(readerSourceData, ReaderSourceData):
			raise TypeError("readerSourceData can be the list ReaderSourceData")

		if sourceCustomCallback and not isinstance(sourceCustomCallback, SourceCustomCallback):
			raise TypeError("sourceCustomCallback can be the list SourceCustomCallback")

		fileSourceCustom = FileSourceCustom()
		for itemFile in readerSourceData.getSourceCustom(sourceCustomCallback):
			# TODO определение типа файла
			fileSourceCustom.custom = itemFile
			statisticObject.makeDocStatisticCustom(source, fileSourceCustom, normalization)

	def createSourceNameIndex(self, statisticObject, readSourceUtils, saveSourceUtils, parseSourceNameCallback):
		"""
		Создание индекса по именам файлов

		:param statisticObject:  объект для создания статистики
		:param readSourceUtils:  объект для чтения данных статистики
		:param saveSourceUtils:  объект для сохранения индекса по статистике
		:param parseSourceNameCallback:  колбэк для обработки имен файлов
		"""
		if not statisticObject:
			raise ParamError("statisticObject cannot be the None-object")
		if not isinstance(statisticObject, Statistic):
			raise TypeError("statisticObject can be the list Statistic")

		if not readSourceUtils:
			raise ParamError("readSourceUtils cannot be the None-object")
		if not isinstance(readSourceUtils, MongoReadUtils):
			raise TypeError("readSourceUtils can be the list MongoReadUtils")

		if not saveSourceUtils:
			raise ParamError("saveSourceUtils cannot be the None-object")
		if not isinstance(saveSourceUtils, MongoSaveUtils):
			raise TypeError("saveSourceUtils can be the list MongoSaveUtils")
		if not ISaveRetrievalUtils.providedBy(saveSourceUtils):
			raise TypeError("saveSourceUtils is not provided by ISaveRetrievalUtils")

		if not parseSourceNameCallback:
			raise ParamError("parseSourceNameCallback cannot be the None-object")
		if not isinstance(parseSourceNameCallback, FileNameNormalization):
			raise TypeError("parseSourceNameCallback can be the list FileNameNormalization")

		for file_data in readSourceUtils.getSubDicts(statisticObject.getMainStatisticID()):
			# получение кортежа '/opt/test dir/file.txt' -> ('/opt/test dir', 'file.txt')
			name_node = os.path.split(file_data['dict_name'])
			try:
				paths = parseSourceNameCallback.normalizeTextWithoutRepetition(name_node[0].encode("utf-8"))
				saveSourceUtils.saveFilename(file_data['_id'], paths, FILENAME_PATH_TYPE)
				names = parseSourceNameCallback.normalizeTextWithoutRepetition(name_node[1].encode("utf-8"))
				saveSourceUtils.saveFilename(file_data['_id'], names, FILENAME_TYPE)
			except IndexError or ParamError as e:  # если вдруг - пустое значение
				pass
