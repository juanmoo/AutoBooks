/* JQuery Script */

// Load People from database //
$(document).ready( function() {

	/* Populate Form Options */
	const URL = "http://localhost:5000/reimbursements?action=get_form_info";
	$.ajax({
		url: URL,
		type: "GET",
		success: populateFrom,
		error: function(result) {
			console.log("There was an error.");
		}
	})

	$("#main_form").submit( submitForm );

})


function submitForm() {

	console.log("The form was submitted!");

}

function populateFrom (response) {
	res = JSON.parse(response);
	console.log(response);

	// Fill User and Officer
	names = res["users"];
	console.log(names);

	$.each(names, function(key, val) {
		$("#user_select").append(
			$("<option>", {
				value: key,
				text: val
			})
		);

		
	});

	// Fill Officers
	officers = res["officers"];
	console.log(officers);

	$.each(officers, function(id, val) {
		$("#officer_select").append(
			$("<option>", {
				value: id,
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
