// Function that takes in county cases and 
// returns the hex color (e.g #FF3F43) associated with it
// with red and green extremes
function getColorRG(cases) {

	return  (cases > 1000000) 	? 	"#ff0000":
			(cases > 100000) 	?	"#ff8000":
			(cases > 10000) 	? 	"#ffff00":
			(cases > 1000)		? 	"#80ff00":
									"#2cba00"
};

// Mono color blue mapper
function getColorMono(cases) {

	return  (cases > 1000000) 	? 	"#08519c":
			(cases > 100000) 	?	"#3182bd":
			(cases > 10000) 	? 	"#6baed6":
			(cases > 1000)		? 	"#bdd7e7":
									"#eff3ff"

}

function getColor(cases) {

	return document.getElementById("monocolor").checked ? getColorMono(cases) : getColorRG(cases)
}

function getFacilityColorMono(count) {
	

	return  (count > 500) 	? 	"#e31a1c":
			(count > 100) 	?	"#fd8d3c":
			(count > 10) 	? 	"#fecc5c":
								"#ffffb2"
}