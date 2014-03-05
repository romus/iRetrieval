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
    def searchData(self, query, customDict, customDictData, mergeDictID):
        """
        Поиск по данным из источников

        :param query:  поисковый запрос
        :param customDict:  словарь с настройками для поиска по именам
        :param customDictData:  настройки для получения данных
        :param mergeDictID:  ID основного словаря
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
        # self.removeFindObject()
        # self._findObject = self._mongoReadUtils.searchFilename(query, customDict, mergeDictID)
        # return self._mongoReadUtils.getSearchData(self._findObject, customDictData)
        return self._search(query, customDict, customDictData, mergeDictID, self._mongoReadUtils.searchFilename)

    def searchData(self, query, customDict, customDictData, mergeDictID):
        """
        Поиск по данным из источников

        :param query:  поисковый запрос c указанием типа, например [тип_запроса, ["test", "search", "inner"]].
        :param customDict:  словарь с настройками для поиска по данным из источников
        :param customDictData:  настройки для получения данных
        :param mergeDictID:  ID основного словаря
        :return:  список найденных документов (может использоваться ленивое получение данных)
        """
        return self._search(query, customDict, customDictData, mergeDictID, self._mongoReadUtils.searchData)

    def removeFindObject(self):
        self._mongoReadUtils.removeSearchData(self._findObject)

    def _search(self, query, customDict, customDictData, mergeDictID, func):
        self.removeFindObject()
        self._findObject = func(query, customDict, mergeDictID)
        return self._mongoReadUtils.getSearchData(self._findObject, customDictData)
