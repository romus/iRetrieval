# -*- coding: utf-8 -*-


__author__ = 'romus'


import zope.interface

from statistic4text.utils.save_utils import MongoSaveUtils
from iRetrieval.errors.errors import ParamError


class ISaveRetrievalUtils(zope.interface.Interface):
	""" Интерфейс """

	def saveFilename(self, dictID, names):
		"""
		Сохранение частей имени источника

		:param dictID:  id источника
		:param names:  список слов, входящих в имя источника
		"""
		pass


class MongoSaveRetrievalUtils(MongoSaveUtils):

	zope.interface.implements(ISaveRetrievalUtils)

	def saveFilename(self, dictID, names):
		"""
		Сохранение частей имени источника

		:param dictID:  id источника
		:param names:  список слов, входящих в имя источника
		"""
		if not dictID:
			raise ParamError("dictID cannot be the None-object")
		if not names:
			raise ParamError("names cannot be the None-object")

		if not isinstance(names, list):
			raise TypeError("names can be the list")

		self._checkExistMergeDict()
		in_d = {"$set": {"names": names}}
		self._filesCollection.update({"_id": dictID}, in_d)
