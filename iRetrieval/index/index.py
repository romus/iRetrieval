# -*- coding: utf-8 -*-


__author__ = 'romus'


from abc import ABCMeta, abstractmethod


class Index():
	""" Класс для создания индекса """

	__metaclass__ = ABCMeta

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

	def createSourceNameIndex(self, customCallback, parseSourceNameCallback, sourceCallback):
		pass

	def createSourceDataIndex(self, readSourceDataCallback):
		pass


