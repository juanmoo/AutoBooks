/* JQuery Script */

// Load People from database //
$(document).ready( function() {
	const URL = "http://localhost:5000/?action=get_form_info";
	$.ajax({
		url: URL,
		type: "GET",
		success: populateFrom,
		error: function(result) {
			console.log("There was an error.");
		}
	})

})


function populateFrom (response) {
	res = JSON.parse(response);
	console.log(response);

	// Fill Name Form
	names = res["users"];
	console.log(names);

	$.each(names, function(key, val) {
		$("#kerberos_select").append(
			$("<option>", {
				value: key,
				text: val
			})
		);
	});

	// Fill Categories
	categories = res["categories"];
	console.log(categories);
	$.each(categories, function(id, name) {
		$("#budget_select").append(
			$("<option>", {
				value: id,
				text: name
			})
		);
	});
}
