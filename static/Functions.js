// Red and green coloring
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
			return Math.round(255 * color).toString(16).padStart(2, '0');   // convert to Hex and prefix "0" if needed
		};
		return `#${f(0)}${f(8)}${f(4)}`;
	}

	return hslToHex(hue, 100, 50);
};

function getColor(val) {

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