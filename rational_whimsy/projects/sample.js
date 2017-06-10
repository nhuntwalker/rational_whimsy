var vis = d3.select("#figure_container"),
	Nboxes = 24,
	blues = ['#225533','#44bbcc','#88dddd','#bbeeff','#0055bb',
	'#334433','#6699aa','#88aaaa','#aacccc','#447799',
	'#225533','#44bbcc','#88dddd','#bbeeff','#0055bb',
	'#334433','#6699aa','#88aaaa','#aacccc','#447799',
	'#225533','#44bbcc','#88dddd','#bbeeff','#0055bb',
	'#334433','#6699aa','#88aaaa','#aacccc','#447799',
	'#225533','#44bbcc','#88dddd','#bbeeff','#0055bb',
	'#334433','#6699aa','#88aaaa','#aacccc','#447799'],

	reds = ['#442222','#aa3333','#cc4433','#ee6633','#ffee55',
	'#661111','#dd1100','#ff0000','#ff4400','#ffff00',
	'#442222','#aa3333','#cc4433','#ee6633','#ffee55',
	'#661111','#dd1100','#ff0000','#ff4400','#ffff00',
	'#442222','#aa3333','#cc4433','#ee6633','#ffee55',
	'#661111','#dd1100','#ff0000','#ff4400','#ffff00',
	'#442222','#aa3333','#cc4433','#ee6633','#ffee55',
	'#661111','#dd1100','#ff0000','#ff4400','#ffff00'];

	greens = ['#335522','#669955','#88aa77','#99cc88','#cceebb',
	'#337711','#55cc33','#88cc55','#88ee55','#bbffaa',
	'#335522','#669955','#88aa77','#99cc88','#cceebb',
	'#337711','#55cc33','#88cc55','#88ee55','#bbffaa',
	'#335522','#669955','#88aa77','#99cc88','#cceebb',
	'#337711','#55cc33','#88cc55','#88ee55','#bbffaa',
	'#335522','#669955','#88aa77','#99cc88','#cceebb',
	'#337711','#55cc33','#88cc55','#88ee55','#bbffaa'],

	allcolors = [blues, reds, greens],
	box_opacity = 0.8;
	
	if (window.innerWidth > 820) {
		var	plotwidth = 800,
			plotheight = 400;
	} else {
		var	plotwidth = window.innerWidth - 20,
			plotheight = plotwidth/2;
	}

vis.attr("width", plotwidth).attr("height", plotheight);
var origData = [];

function plotBoxes(){
	// Define rectangles
	jj = Math.round(Math.random()*2)
	
	var jsonSquares = [];
	for (var ii=0; ii < Nboxes; ii++) {
		var x = Math.random()*plotwidth,
			y = Math.random()*plotheight,
			width = Math.random()*(plotwidth/4)+50,
			height = Math.random()*(plotheight/4)+50,
			color = allcolors[jj][ii];
	
		jsonSquares.push(
		{"xcoord":x, "ycoord":y, "width":width, "height":height, "color":color});
	}
	origData.push(jsonSquares);
	
	var squares = vis.selectAll("rect")
		.data(jsonSquares)
		.enter()
		.append("rect");
	
	var squareAttributes = squares
		.attr("x", function(d){return d.xcoord;})
		.attr("y", function(d){return d.ycoord;})
		.attr("width", function(d){return d.width;})
		.attr("height", function(d){return d.height;})
		.attr("fill", function(d){return d.color;})
		.attr("opacity", box_opacity)
		.attr("original", function(d){
			return {x: d.xcoord, y: d.ycoord, width: d.width, height: d.height};
		});
}
plotBoxes();

function resizeSvg(){
	
	var windowWidth = window.innerWidth,
		ratio = windowWidth/plotwidth;
	
	if (windowWidth < 800) {
		var svgWidth = windowWidth - 20,
			svgHeight = svgWidth/2;
		
		vis.attr("width", svgWidth).attr("height", svgHeight);
		
		
		var squares = vis.selectAll("rect");
	
		var squareAttributes = squares
			.attr("x", function(d){return d.xcoord * ratio})
			.attr("y", function(d){return d.ycoord * ratio})
			.attr("width", function(d){return d.width * ratio})
			.attr("height", function(d){return d.height * ratio});
		
	}
}

jQuery(window).resize(
	function(){
		resizeSvg();
	}
);