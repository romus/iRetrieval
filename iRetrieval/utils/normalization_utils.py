# -*- coding: utf-8 -*-


__author__ = 'romus'


import os
import re

from statistic4text.errors.errors import ParamError
from statistic4text.utils.normalization_utils import SimpleNormalization


class FileNameNormalization(SimpleNormalization):
	""" Класс для нормализации имен источников """

	def __init__(self):
		super(FileNameNormalization, self).__init__()

	def normalizeText(self, text):
		"""
		Нормализация пути к файлу в файловой системе

		:param text:  имя файла или путь к файлу
		:return: список нормализованных слов
		"""
		if not text:
			raise ParamError("Text is not to be the None-object or ''")

		dt = self._detectEncoding.encodeText(text, self._defaultEncodeText)  # dt = decode text
		normalize_words = []  # normalize words

		# разбиение пути на составляющие, например /opt/test dir -> ['', 'opt', 'test dir']
		for item in dt.split(os.path.sep):
			# разбиение составлющих на слова, например 'test dir' -> ['test', 'dir']
			temp_items = re.split('\s+', item)
			for temp_item in temp_items:
				if temp_item:
					normalize_words.append(temp_item)

		user_decode_words = []
		if self._defaultEncodeText == self.getNormalizeTextEncode():
			user_decode_words = normalize_words
		else:
			for normalize_word in normalize_words:
				user_decode_words.append(self._detectEncoding.encodeText(normalize_word, self.getNormalizeTextEncode()))

		return user_decode_words
