# -*- coding: utf-8 -*-


__author__ = 'romus'


import pymongo
import zope.interface

from statistic4text.utils.save_utils import MongoSaveUtils
from iRetrieval.errors.errors import ParamError


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
		"""
		pass


class MongoSaveRetrievalUtils(MongoSaveUtils):

	INDEX_FIELDS_SOURCE_NAME_COLLECTION = [("name", pymongo.DESCENDING), ("dict_id", pymongo.DESCENDING),
										   ("file_name_type", pymongo.DESCENDING)]
	zope.interface.implements(ISaveRetrievalUtils)

	def __init__(self, host, port, user, password, databaseName, filesCollectionName, dataFilesCollectionName,
				 sourceNameCollection, mergeDictName="merge_dict", isDeleteAll=False):
		super(MongoSaveRetrievalUtils, self).__init__(host, port, user, password, databaseName, filesCollectionName,
													  dataFilesCollectionName, mergeDictName, isDeleteAll)
		self.__sourceNameCollection = self._db[sourceNameCollection]

		if isDeleteAll:
			self.__sourceNameCollection.remove()

		# создание индекса по новым коллекциям
		if len(self.INDEX_FIELDS_SOURCE_NAME_COLLECTION) > 0:
			self.__sourceNameCollection.create_index(self.INDEX_FIELDS_SOURCE_NAME_COLLECTION)

		self.__type_name = [FILENAME_TYPE, FILENAME_PATH_TYPE]

	def saveFilename(self, dictID, names, fileNamesType):
		"""
		Сохранение частей имени источника

		:param dictID:  id источника
		:param names:  список слов, входящих в имя источника
		:param fileNamesType:  тип имени источника
		"""
		if not dictID:
			raise ParamError("dictID cannot be the None-object")
		if not names:
			raise ParamError("names cannot be the None-object")
		if not fileNamesType:
			raise ParamError("fileNamesType cannot be the None-object")

		if not isinstance(names, list):
			raise TypeError("names can be the list list")
		if not isinstance(fileNamesType, int):
			raise TypeError("fileNamesType can be the list int")

		if not fileNamesType in self.__type_name:
			raise TypeError("unsupported fileNamesType")

		for name in names:
			self.__sourceNameCollection.insert({"name": name, "dict_id": dictID, "file_name_type": fileNamesType})

	def deleteDicts(self):
		""" Помимо данных из основных коллекций, данные удаляются еще и из коллекции  sourceNameCollection"""
		super(MongoSaveRetrievalUtils, self).deleteDicts()
		# TODO необходимо удалять не все данные, а только созданные объектом данного класса
		self.__sourceNameCollection.remove()
