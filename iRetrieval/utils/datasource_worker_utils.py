# -*- coding: utf-8 -*-


__author__ = 'romus'


from abc import ABCMeta, abstractmethod


class DataSourceWorker():
	""" Класс для создания статистики по источникам и данным из этих источников """

	__metaclass__ = ABCMeta

	@abstractmethod
	def createStatistics(self, statisticObject, readerSourceData):
		"""
		Создание статистики по объектам и данным из файловой системы

		:param statisticObject:  объект для создания статистики
		:param readerSourceData:  объект для получения настроект для работы с источниками
		"""
		pass


class DataSourceWorkerFS(DataSourceWorker):
	""" Класс для создания статистики по файлам (работа с файловой системой) """

	def __init__(self):
		pass

	def createStatistics(self, statisticObject, readerSourceData):
		"""

		:param statisticObject:  объект для создания статистики
		:param readerSourceData:  объект для получения полных путей к файлам
		"""
		pass
