/**
 * User: romus
 * Date: 08.11.13
 * Time: 13:09
 */


function map() {
    // В качестве глобольного параметра используется q - выражение с запросом  [[слово1, слово2], [слово3, ...], ...]
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
				dictName: this.dictName
			};
			emit(this._id, temp_value);
		}
	}
}
