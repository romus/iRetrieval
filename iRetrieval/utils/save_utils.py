# -*- coding: utf-8 -*-


__author__ = 'romus'

import zope.interface

from statistic4text.utils.save_utils import MongoSaveUtils
from iRetrieval.errors.errors import ParamError


class ISaveRetrievalUtils(zope.interface.Interface):
    """ Интерфейс """

    def saveFilename(self, dictID, names, simpleDictName):
        """
        Сохранение частей имени источника

        :param dictID:  id источника
        :param names:  список слов, входящих в имя источника
        :param simpleDictName:  упрощенное имя истоника (для поиска по точному совпадению)
        """
        pass


class MongoSaveRetrievalUtils(MongoSaveUtils):

    zope.interface.implements(ISaveRetrievalUtils)

    def saveFilename(self, dictID, names, simpleDictName):
        """
        Сохранение частей имени источника

        :param dictID:  id источника
        :param names:  список слов, входящих в имя источника
        :param simpleDictName:  упрощенное имя истоника (для поиска по точному совпадению)
        """
        if not dictID:
            raise ParamError("dictID cannot be the None-object")
        if not names:
            raise ParamError("names cannot be the None-object")
        if not simpleDictName:
            raise ParamError("simpleDictName cannot be the None-object or empty")

        if not isinstance(names, list):
            raise TypeError("names can be the list")

        self._checkExistMergeDict()
        in_d = {"$set": {"names": names, "simple_name": simpleDictName}}
        self._filesCollection.update({"_id": dictID}, in_d)
