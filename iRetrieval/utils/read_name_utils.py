# -*- coding: utf-8 -*-


__author__ = 'romus'


from os import walk
from os.path import join
from abc import ABCMeta, abstractmethod
from iRetrieval.errors.errors import ParamError


class ReaderName():
	""" Класс для чтения имен источников """

	__metaclass__ = ABCMeta

	@abstractmethod
	def getSourceName(self):
		"""
		Получение имен источников (lazy)

		:rtype:  tuple
		:return:  имя источника в неизмененной кодировке
		"""
		return None


class ReaderNameFS(ReaderName):

	def __init__(self, listPaths):
		"""
		Инициализация

		:param listPaths:  список путей файловой системы для получения имен файлов
		"""
		if not listPaths:
			raise ParamError("listPaths can't to be a None or empty")
		if not isinstance(listPaths, list):
			raise TypeError("listPaths can to be a list type")

		self.__listPaths = listPaths

	def getSourceName(self):
		for itemPath in self.__listPaths:
			for root, dirName, fileNames in walk(itemPath):
				for itemFileName in fileNames:
					yield join(root, itemFileName)
