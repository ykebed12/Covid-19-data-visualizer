// Function that takes in county cases and 
// returns the hex color (e.g #FF3F43) associated with it
// with red and green extremes
function getColorRG(cases) {

	return  (cases > 1000000) 	? 	"#ff0000":
			(cases > 100000) 	?	"#ff8000":
			(cases > 10000) 	? 	"#ffff00":
			(cases > 1000)		? 	"#80ff00":
									"#00ff00"
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

function makeLegend (map) {

	var div = L.DomUtil.create('div', 'info legend'),
		grades = [0, 1000, 10000, 100000, 1000000]

	// loop through our intervals and generate a label with a colored square for each interval
	for (var i = 0; i < grades.length; i++) {
		div.innerHTML += '<i style="background:' + getColor(grades[i] + 1) + '"></i> ' +
			grades[i] + (grades[i + 1] ? '&ndash;' + grades[i + 1] + '<br>' : '+');
	}

	return div;
};

