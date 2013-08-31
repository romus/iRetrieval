# -*- coding: utf-8 -*-


__author__ = 'romus'


from os import walk
from os.path import join
from abc import ABCMeta, abstractmethod
from iRetrieval.errors.errors import ParamError


class ReaderSourceData():
	""" Класс для чтения данных по источникам """

	__metaclass__ = ABCMeta

	@abstractmethod
	def getSourceCustom(self, sourceCustomCallback=None):
		""" Получение данных по источнику (lazy) """
		yield None


class SourceCustomCallback():

	__metaclass__ = ABCMeta

	@abstractmethod
	def checkSourceCustom(self, sourceCustom):
		"""
		Проверка данных из источника

		:param sourceCustom:  данные источника
		:return:  True - проверка пройдена
		"""
		return False


class ReaderNameFS(ReaderSourceData):

	def __init__(self, listPaths):
		"""
		Инициализация

		:param listPaths:  список путей файловой системы для получения имен файлов
		"""
		if not listPaths:
			raise ParamError("listPaths can't to be a None or empty")
		if not isinstance(listPaths, list):
			raise TypeError("listPaths can to be the list type")

		self.__listPaths = listPaths

	def getSourceCustom(self, checkSourceCustomCallback=None):
		"""
		Получение данных по источнику (lazy)

		Для файловой системы - это путь к файлу в неизменненой кодировке
		"""
		if checkSourceCustomCallback:
			if not isinstance(checkSourceCustomCallback, FSSourceCustomCallback):
				raise TypeError("checkSourceCustomCallback can to be the FSSourceCustomCallback type")

		for itemPath in self.__listPaths:
			for root, dirName, fileNames in walk(itemPath):
				for itemFileName in fileNames:
					if checkSourceCustomCallback:
						if checkSourceCustomCallback.checkSourceCustom(itemFileName):
							yield join(root, itemFileName)
					else:
						yield join(root, itemFileName)


class FSSourceCustomCallback(SourceCustomCallback):

	def __init__(self, protectEnds=None):
		"""
		Инициализация

		:param protectEnds:  запрещенные расширения файлов,
			при None = [".c", ".cpp", ".py", ".java", ".html", ".css", ".zip"]
		:raise:  при передачачи аргумента не типа list
		"""
		if protectEnds:
			if not isinstance(protectEnds, list):
				raise TypeError("protectEnds can to be the list type")
			self.__protectEnds = protectEnds
		else:
			self.__protectEnds = [".c", ".cpp", ".py", ".java", ".html", ".css", ".zip"]

	def checkSourceCustom(self, sourceCustom):
		for end in self.__protectEnds:
			if sourceCustom.endswith(end):
				return False
		return True
