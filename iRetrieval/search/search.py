# -*- coding: utf-8 -*-


__author__ = 'romus'


from abc import ABCMeta, abstractmethod


class Search():
	""" Класс для поиска по индексу """

	__metaclass__ = ABCMeta

	@abstractmethod
	def searchNames(self, query):
		"""
		Поиск по именам источников

		:param query:  поисковый запрос
		:return:  список найденных документов
		"""
		return None

	@abstractmethod
	def searchData(self, query):
		"""
		Поиск по данным из источников

		:param query:  поисковый запрос
		:return:  список найденных документов
		"""
		return None


class MongoSearch(Search):

	def __init__(self):
		pass

	def searchNames(self, query):
		return None

	def searchData(self, query):
		return None
