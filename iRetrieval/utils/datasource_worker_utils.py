# -*- coding: utf-8 -*-


__author__ = 'romus'

import os
import magic
from abc import ABCMeta, abstractmethod

from statistic4text.statistic.statistic import Statistic
from statistic4text.utils.save_utils import MongoSaveUtils
from statistic4text.utils.read_utils import MongoReadUtils
from statistic4text.utils.normalization_utils import DetectEncoding
from statistic4text.utils.source_data_utils import FileSourceCustom
from statistic4text.utils.source_data_utils import FILE_BLOCK_SOURCE_TYPE

from iRetrieval.errors.errors import ParamError
from iRetrieval.utils.save_utils import ISaveRetrievalUtils
from iRetrieval.utils.source_data_utils import SourceFactoryImpl, OF_FILE_SOURCE
from iRetrieval.utils.normalization_utils import FileNameNormalization
from iRetrieval.utils.read_datasource_utils import ReaderSourceData, SourceCustomCallback


MIME_TEXT = "text/plain"
MIME_WORD = "application/msword"


class DataSourceWorker():
    """ Класс для создания статистики по источникам и данным из этих источников """

    __metaclass__ = ABCMeta

    @abstractmethod
    def createStatistics(self, statisticObject, readerSourceData, normalization, sourceCustomCallback=None):
        """
        Создание статистики по объектам и данным из файловой системы

        :param statisticObject:  объект для создания статистики
        :param readerSourceData:  объект для получения настроект для работы с источниками
        :param normalization:  объект для нормализации данных
        :param sourceCustomCallback:  колбэк для объекта получения настроек
        """
        pass

    @abstractmethod
    def createSourceNameIndex(self, statisticObject, readSourceUtils, saveSourceUtils, parseSourceNameCallback):
        """
        Создание индекса по названим источников

        :param statisticObject:  объект для создания статистики
        :param readSourceUtils:  объект для чтения данных статистики
        :param saveSourceUtils:  объект для сохранения индекса по статистике
        :param parseSourceNameCallback:  колбэк для обработки имен источников
        """
        pass


class DataSourceWorkerFS(DataSourceWorker):
    """ Класс для создания статистики по файлам (работа с файловой системой) """

    def __init__(self):
        source_factory = SourceFactoryImpl()
        self._source = {'text': source_factory.createSource(FILE_BLOCK_SOURCE_TYPE),
                        'word': source_factory.createSource(OF_FILE_SOURCE)}

    def createStatistics(self, statisticObject, readerSourceData, normalization, sourceCustomCallback=None):
        """

        :param statisticObject:  объект для создания статистики
        :param readerSourceData:  объект для получения полных путей к файлам
        :param normalization:  объект для нормализации данных
        :param sourceCustomCallback:  колбэк для объекта получения настроек (верификация путей)
        """
        if not statisticObject:
            raise ParamError("statisticObject cannot be the None-object")
        if not isinstance(statisticObject, Statistic):
            raise TypeError("statisticObject can be the list Statistic")

        if not readerSourceData:
            raise ParamError("readerSourceData cannot be the None-object")
        if not isinstance(readerSourceData, ReaderSourceData):
            raise TypeError("readerSourceData can be the list ReaderSourceData")

        if sourceCustomCallback and not isinstance(sourceCustomCallback, SourceCustomCallback):
            raise TypeError("sourceCustomCallback can be the list SourceCustomCallback")

        de_object = DetectEncoding()
        fileSourceCustom = FileSourceCustom()
        for itemFile in readerSourceData.getSourceCustom(sourceCustomCallback):
            file_type = magic.from_file(itemFile.decode(de_object.getEncode(itemFile)), mime=True)
            fileSourceCustom.custom = itemFile

            source = None
            if file_type == MIME_TEXT:
                source = self._source['text']
            elif file_type == MIME_WORD:
                source = self._source['word']

            if source:
                statisticObject.makeDocStatisticCustom(source, fileSourceCustom, normalization)

    def createSourceNameIndex(self, statisticObject, readSourceUtils, saveSourceUtils, parseSourceNameCallback):
        """
        Создание индекса по именам файлов

        :param statisticObject:  объект для создания статистики
        :param readSourceUtils:  объект для чтения данных статистики
        :param saveSourceUtils:  объект для сохранения индекса по статистике
        :param parseSourceNameCallback:  колбэк для обработки имен файлов
        """
        if not statisticObject:
            raise ParamError("statisticObject cannot be the None-object")
        if not isinstance(statisticObject, Statistic):
            raise TypeError("statisticObject can be the list Statistic")

        if not readSourceUtils:
            raise ParamError("readSourceUtils cannot be the None-object")
        if not isinstance(readSourceUtils, MongoReadUtils):
            raise TypeError("readSourceUtils can be the list MongoReadUtils")

        if not saveSourceUtils:
            raise ParamError("saveSourceUtils cannot be the None-object")
        if not isinstance(saveSourceUtils, MongoSaveUtils):
            raise TypeError("saveSourceUtils can be the list MongoSaveUtils")
        if not ISaveRetrievalUtils.providedBy(saveSourceUtils):
            raise TypeError("saveSourceUtils is not provided by ISaveRetrievalUtils")

        if not parseSourceNameCallback:
            raise ParamError("parseSourceNameCallback cannot be the None-object")
        if not isinstance(parseSourceNameCallback, FileNameNormalization):
            raise TypeError("parseSourceNameCallback can be the list FileNameNormalization")

        for file_data in readSourceUtils.getSubDicts(statisticObject.getMainStatisticID()):
            # получение кортежа '/opt/test dir/file.txt' -> ('/opt/test dir', 'file.txt')
            name_node = os.path.split(file_data['dict_name'])
            try:
                paths = parseSourceNameCallback.normalizeTextWithoutRepetition(name_node[0].encode("utf-8"))
                names = parseSourceNameCallback.normalizeTextWithoutRepetition(name_node[1].encode("utf-8"))
                names.extend(paths)
                saveSourceUtils.saveFilename(file_data['_id'], list(set(names)), name_node[1])
            except IndexError or ParamError:  # если вдруг - пустое значение
                pass
