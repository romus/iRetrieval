# -*- coding: utf-8 -*-


__author__ = 'romus'


import zope.interface
from bson.code import Code
from pymongo.collection import Collection

from statistic4text.utils.read_utils import MongoReadUtils

from iRetrieval.utils.map_reduce_js import *
from iRetrieval.errors.errors import ParamError


class ISearchRetrievalUtils(zope.interface.Interface):
    """ Интерфейс """

    def searchFilename(self, q, customDict, mergeDictID):
        """
        Поиск по именам источников

        @param q:  запрос с указанием типа
        @param customDict:  словарь с настройками для поиска по именам
        @param mergeDictID:  ID основного словаря
        @return:  объект, для последующего получения данных
        """
        return None

    def searchData(self, q, customDict, mergeDictID):
        """
        Поиск по данным из источников

        @param q:  поисковый запрос c указанием типа
        @param customDict:  словарь с настройками для поиска по данным из источников
        @param mergeDictID:  ID основного словаря
        @return:  объект, для последующего получения данных
        """
        return None

    def getSearchData(self, findObject, customDict):
        """
        Получение данных по поисковому запросу

        @param findObject:  объект, полученный searchFilename(...)
        @param customDict:  настройки для получения данных
        @return:  данные по поисковому запросу
        """
        return None


class MongoSearchRetrievalUtils(MongoReadUtils):

    zope.interface.implements(ISearchRetrievalUtils)

    def __init__(self, host, port, user, password, databaseName, filesCollectionName, dataFilesCollectionName):
        super(MongoSearchRetrievalUtils, self).__init__(host, port, user, password, databaseName, filesCollectionName,
                                                        dataFilesCollectionName)
        # обязательные ключи для работы поиска и получение данных по поиску
        self._customKeysSearch = ["result_cn"]
        self._customKeysData = ["is_lazy"]

    def searchFilename(self, q, customDict, mergeDictID):
        """
        Поиск по именам источников

        @param q: запрос с указанием типа - [1, [[слово1, слово2], [слово3, ...], ...] ("запрос")]
        @param customDict:  обязательные параметры - result_cn - имя коллекции
        @param mergeDictID:  ID основного словаря
        @return:  объект коллекции с найденными источниками
        """
        self._checkType(q, customDict, mergeDictID)

        query = {"dict_type": 1, "merge_dict_id": mergeDictID}  # поисковый запрос
        s = {"q": q[1], "type_q": q[0]}  # переменные видимые внутри js-функций
        mapper = Code(mapFunction)
        reducer = Code(reduceFunction)
        return self._filesCollection.map_reduce(mapper, reducer, customDict['result_cn'], query=query, scope=s)

    def searchData(self, q, customDict, mergeDictID):
        """
        Поиск по данным из источников

        @param q:  поисковый запрос c указанием типа, например [тип_запроса, ["test", "search", "inner"]]. Тип запроса
                   не учитавается
        @param customDict:  словарь с настройками для поиска по данным из источников  result_cn - имя коллекции
        @param mergeDictID:  ID основного словаря
        @return:  объект, для последующего получения данных
        """
        self._checkType(q, customDict, mergeDictID)

        # для получения данных по сессии с mergeDictID и не включая данные по общей статистике
        query = {"merge_dict_id": mergeDictID, "dict_id": {"$ne": mergeDictID}}
        scope = {"q": q[1]}  # переменные видимые внутри js-функций
        mapper = Code(mapFunctionData)
        reducer = Code(reduceFunctionData)
        return self._dataFilesCollection.map_reduce(mapper, reducer, customDict['result_cn'], query=query, scope=scope)

    def getSearchData(self, findObject, customDict):
        """
        Получение данных по поисковому запросу

        @param findObject:  объект, полученный searchFilename(...)
        @param customDict:  настройки для получения данных, порамерт is_lazy - True (ленивое получение данных)
        @return:  данные по поисковому запросу
        """
        if not findObject:
            raise ParamError("findObject cannot be the None-object")
        if not customDict:
            raise ParamError("customDict cannot be the None-object or empty")

        if not isinstance(findObject, Collection):
            raise TypeError("findObject can be the Collection")
        if not isinstance(customDict, dict):
            raise TypeError("customDict can be the dict")

        # проверка наличие необходимых значений
        for key in self._customKeysData:
            if key not in customDict:
                raise KeyError("key = " + key + " not found")

        if customDict['is_lazy']:
            return self._getLazyData(findObject, {})
        return findObject.find()

    def removeSearchData(self, findObject):
        """
        Удаление найденных по запросу результатов.

        Временно
        @param findObject:  объект, полученный searchFilename(...)
        """
        if findObject:
            findObject.remove()

    def _checkType(self, q, customDict, mergeDictID):
        """ Проверка типов переданных значений """
        if not q:
            raise ParamError("q cannot be the None-object or empty")
        if not customDict:
            raise ParamError("customDict cannot be the None-object or empty")
        if not mergeDictID:
            raise ParamError("mergeDictID cannot be the None-object or empty")

        if not isinstance(q, list):
            raise TypeError("q can be the list")
        if not isinstance(customDict, dict):
            raise TypeError("customDict can be the dict")

        # проверка наличие необходимых значений
        for key in self._customKeysSearch:
            if key not in customDict:
                raise KeyError("key = " + key + " not found")
