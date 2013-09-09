# -*- coding: utf-8 -*-


__author__ = 'romus'


from abc import ABCMeta, abstractmethod
from statistic4text.statistic.statistic import Statistic
from statistic4text.utils.source_data_utils import FileSourceCustom
from iRetrieval.errors.errors import ParamError
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
		if not readerSourceData:
			raise  ParamError("readerSourceData cannot be the None-object")

		if not isinstance(statisticObject, Statistic):
			raise TypeError("statisticObject can be the list Statistic")
		if not isinstance(readerSourceData, ReaderSourceData):
			raise TypeError("readerSourceData can be the list ReaderSourceData")
		if sourceCustomCallback and not isinstance(sourceCustomCallback, SourceCustomCallback):
			raise TypeError("sourceCustomCallback can be the list SourceCustomCallback")

		fileSourceCustom = FileSourceCustom()
		for itemFile in readerSourceData.getSourceCustom(sourceCustomCallback):
			# TODO определение типа файла
			fileSourceCustom.custom = itemFile
			statisticObject.makeDocStatisticCustom(source, fileSourceCustom, normalization)
