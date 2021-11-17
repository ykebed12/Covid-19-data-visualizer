// Red and green coloring based on some value from 0 to 1
function hexColorRatio(value) {
	//value from 0 to 1
	var hue = ((1 - value) * 120);

	// ["hsl(", hue, ",100%,50%)"].join("");
	function hslToHex(h, s, l) {
		l /= 100;
		const a = s * Math.min(l, 1 - l) / 100;
		const f = n => {
			const k = (n + h / 30) % 12;
			const color = l - a * Math.max(Math.min(k - 3, 9 - k, 1), -1);
			return Math.round(255 * color).toString(16).padStart(2, '0');  
			// convert to Hex and prefix "0" if needed
		};
		return `#${f(0)}${f(8)}${f(4)}`;
	}

	return hslToHex(hue, 100, 50);
};

// Function that takes in county cases and 
// returns the hex color (e.g #FF3F43) associated with it
// with red and green extremes
function getColor(val) {

	// 10000+ cases will be red
	// and 0 cases will be green
	ratio = (val > 10000) ? 1.0: (val / 10000.0);
	return hexColorRatio(ratio);
};

function style(feature) {
    return {
        fillColor: getColor(s),
        weight: 2,
        opacity: 1,
        color: 'white',
        dashArray: '3',
        fillOpacity: 0.7
    };
};