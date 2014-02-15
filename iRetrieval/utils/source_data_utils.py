# -*- coding: utf-8 -*-


__author__ = 'romus'

import os

from docx import opendocx, getdocumenttext

from statistic4text.utils.source_data_utils import FileSource, SourceFactory


OF_FILE_SOURCE = "office_file_source"


class OfficeFileSource(FileSource):
    """ Источник для работы с офисными документами"""

    def openSource(self, custom):
        """
        Открыть документ для работы

        :param custom:  полный путь к файлу
        :return:  [документ, имя_документа]
        """
        return [opendocx(custom), custom]

    def closeSource(self, source):
        """ Источник закрывается внутри библиотеки """
        pass

    def read(self, source):
        if not source:
            raise Exception("Source not found")
        if not isinstance(source, list):
            raise TypeError("source can be the list")

        para_text_list = getdocumenttext(source[0])
        for para_text in para_text_list:
            yield para_text

    def getName(self, source):
        return os.path.abspath(source[1])

    def getSourceSize(self, source):
        return os.path.getsize(os.path.abspath(source[1])) / 1024

    def getSourceDateCreated(self, source):
        return os.path.getctime(os.path.abspath(source[1]))

    def getSourceDateModified(self, source):
        return os.path.getmtime(os.path.abspath(source[1]))


class SourceFactoryImpl(SourceFactory):

    def createSource(self, source_type):
        """
        Создание объекта для работы с истоником данных

        :param source_type:  тип источника данных
        :return:  объект для работы с источником данных
        """
        return OfficeFileSource() if source_type == OF_FILE_SOURCE else SourceFactory.createSource(self, source_type)
