# -*- coding: utf-8 -*-


__author__ = 'romus'


import zope.interface
from statistic4text.utils.save_utils import MongoSaveUtils


FILENAME_TYPE = 1  # только имя файла
FILENAME_PATH_TYPE = 2  # путь к файлу


class ISaveRetrievalUtils(zope.interface.Interface):
	""" Интерфейс """

	def saveFilename(self, dictID, names, fileNamesType):
		"""
		Сохранение частей имени источника

		:param dictID:  id источника
		:param names:  список слов, входящих в имя источника
		:param fileNamesType:  тип имени источника
		:return:
		"""
		return -1


class MongoSaveRetrievalUtils(MongoSaveUtils):

	zope.interface.implements(ISaveRetrievalUtils)

	def __init__(self, host, port, user, password, databaseName, filesCollectionName, dataFilesCollectionName,
				 sourceNameCollection, mergeDictName="merge_dict", isDeleteAll=False):
		super(MongoSaveRetrievalUtils, self).__init__(host, port, user, password, databaseName, filesCollectionName,
													  dataFilesCollectionName, mergeDictName, isDeleteAll)
		self.__sourceNameCollection = self._db[sourceNameCollection]

		if isDeleteAll:
			self.__sourceNameCollection.remove()

	def saveFilename(self, dictID, names, fileNamesType):
		"""
		Сохранение частей имени источника

		:param dictID:  id источника
		:param names:  список слов, входящих в имя источника
		:param fileNamesType:  тип имени источника
		:return:
		"""
		return -1
