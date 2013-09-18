# -*- coding: utf-8 -*-


__author__ = 'romus'


from abc import ABCMeta, abstractmethod


FILENAME_TYPE = 1  # только имя файла
FILENAME_PATH_TYPE = 2  # путь к файлу


class SaveRetrievalUtils():

	__metaclass__ = ABCMeta

	@abstractmethod
	def saveFilename(self, dictID, names, fileNamesType):
		"""
		Сохранение частей имени источника

		:param dictID:  id источника
		:param names:  список слов, входящих в имя источника
		:param fileNamesType:  тип имени источника
		:return:
		"""
		return -1
