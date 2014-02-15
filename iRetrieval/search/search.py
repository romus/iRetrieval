# -*- coding: utf-8 -*-


__author__ = 'romus'

from abc import ABCMeta, abstractmethod

from statistic4text.utils.read_utils import MongoReadUtils

from iRetrieval.errors.errors import ParamError
from iRetrieval.utils.read_utils import ISearchRetrievalUtils


class Search():
    """ Класс для поиска по индексу """

    __metaclass__ = ABCMeta

    @abstractmethod
    def searchNames(self, query, customDict, customDictData, mergeDictID):
        """
        Поиск по именам источников

        :param query:  поисковый запрос
        :param customDict:  словарь с настройками для поиска по именам
        :param customDictData:  настройки для получения данных
        :param mergeDictID:  ID основного словаря
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

    def __init__(self, mongoReadUtils):
        """
        Инициализация

        :param mongoReadUtils:  параметр для чтения и поиска данных в mongodb
        """
        if not mongoReadUtils:
            raise ParamError("mongoReadUtils cannot be the None-object")
        if not isinstance(mongoReadUtils, MongoReadUtils):
            raise TypeError("mongoReadUtils can be the list MongoReadUtils")
        if not ISearchRetrievalUtils.providedBy(mongoReadUtils):
            raise TypeError("mongoReadUtils is not provided by ISearchRetrievalUtils")

        self._mongoReadUtils = mongoReadUtils
        self._findObject = None

    def searchNames(self, query, customDict, customDictData, mergeDictID):
        """
        Поиск по именам источников

        :param query:  поисковый запрос, пример запроса [TYPE_Q_LOGIC, [["doc"], ["doc"]]]
        :param customDict:  словарь с настройками для поиска по именам
        :param customDictData:  настройки для получения данных
        :param mergeDictID:  ID основного словаря
        :return:  список найденных документов (может использоваться ленивое получение данных)
        """
        self.removeFindObject()
        self._findObject = self._mongoReadUtils.searchFilename(query, customDict, mergeDictID)
        return self._mongoReadUtils.getSearchData(self._findObject, customDictData)

    def searchData(self, query):
        return None

    def removeFindObject(self):
        self._mongoReadUtils.removeSearchData(self._findObject)
