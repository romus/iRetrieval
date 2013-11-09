/**
 * User: romus
 * Date: 08.11.13
 * Time: 13:09
 */


function reduce(key, values) {
	var total = 0;
	for (var i = 0; i < values.length; i++) {
		total += values[i].count;
	}
	return {count: total, dictName: values[0].dictName};
}
