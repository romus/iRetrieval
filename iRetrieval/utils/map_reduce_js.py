# -*- coding: utf-8 -*-


__author__ = 'romus'


mapFunction = """
		function map() {
			// В качестве глобольного параметра используется:
			// q - выражение с запросом  [[слово1, слово2], [слово3, ...], ...],
			// type_q - тип поискового запроса - 0 - логический запрос, 1 - точный запрос

			if (type_q == 0) {
				for (var i = 0; i < q.length; i++) {
					var is_found = 0;
					for (var j = 0; j < q[i].length; j++) {
						if (this.names.indexOf(q[i][j]) == -1) {
							is_found = 0;
							break;
						} else {
							is_found = 1;
						}
					}

					if (is_found == 1) {
						var temp_value = {
							count: 1,
							dictName: this.dict_name,
							simple_name: this.simple_name
						};
						emit(this._id, temp_value);
					}
				}
			}  else if (type_q == 1 && this.simple_name.valueOf() == q.valueOf()) {
				var temp_value = {
					count: 1,
					dictName: this.dict_name,
					simple_name: this.simple_name
				};
				emit(this._id, temp_value);
			}
		}
	"""

reduceFunction = """
		function reduce(key, values) {
			var total = 0;
			for (var i = 0; i < values.length; i++) {
				total += values[i].count;
			}
			return {count: total,
					dictName: values[0].dictName,
					simple_name: values[0].simple_name};
		}
	"""
