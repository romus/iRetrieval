# -*- coding: utf-8 -*-


__author__ = 'romus'


import re
import unicodedata
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
		:return: спикок свой из пути
		"""
		if not text:
			raise ParamError("Text is not to be the None-object or ''")

		if not isinstance(text, str):
			raise TypeError("text can be the list str")

		dt = self._detectEncoding.encodeText(text, self._defaultEncodeText)  # dt = decode text
		ndt = self._diacritics.sub('', unicodedata.normalize('NFD', unicode(dt, self._defaultEncodeText)))
		ndt = ndt.lower().replace("\n", " ").strip()

		n_w = []  # normalize words
		if ndt:
			split_words = ndt.split('/')  # убрать символ пути
			for word in split_words:
				temp_words = re.split('\s+', word)  # убрать пробелы из слова
				for temp_word in temp_words:
					if temp_word:
						n_w.append(temp_word)
		else:
			try:
				n_w = re.split('\s+', ndt)
			except Exception as e:
				print("Error parse {0}".format(str(e)))

		return [self._detectEncoding.encodeText(item.encode(self._defaultEncodeText), self.getNormalizeTextEncode()) for item in n_w]
