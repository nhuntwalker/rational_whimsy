/*
* Author: Nicholas Hunt-Walker
* Created: Feb 4, 2015
*/

/*********************
* Setup interest form
*********************/
jQuery(document).ready(function(){
dom = document;

var input1 = dom.createElement("input"),
	label1 = dom.createElement("label"),

	input2 = dom.createElement("input"),
	label2 = dom.createElement("label"),

	input3 = dom.createElement("input"),
	label3 = dom.createElement("label"),

	input4 = dom.createElement("input"),
	label4 = dom.createElement("label"),

	clearfix = dom.createElement("div"),

	errbox = dom.createElement("div"),
	submit = dom.createElement("button"),

	break1 = dom.createElement("br"),
	break2 = dom.createElement("br"),
	break3 = dom.createElement("br"),
	break4 = dom.createElement("br"),

	innerDiv1 = dom.createElement("div"),
	innerDiv2 = dom.createElement("div"),

	theForm = dom.createElement("form"),
	formDiv = dom.createElement("div");

label1["for"] = "money_input";
label1.textContent = "Principal ($)";

input1.type = "number";
input1.placeholder = "Principal";
input1.value = 5000;
input1.id = "money_input";

label2["for"] = "rate_input";
label2.textContent = "Interest Rate (%)";

input2.type = "number";
input2.placeholder = "Interest Rate";
input2.value = 7;
input2.id = "rate_input";

label3["for"] = "time_input";
label3.textContent = "Term Length (Yrs)";

input3.type = "number";
input3.placeholder = "Term Length";
input3.value = 30;
input3.id = "time_input";

label4["for"] = "monthly_input";
label4.textContent = "Monthly Contribution ($)";

input4.type = "number";
input4.placeholder = "Contribution";
input4.value = 400;
input4.id = "monthly_input";

errbox.id = "errbox"

submit.textContent = "Submit";
submit.id = "submit";

jQuery(innerDiv1).addClass("calcform_inner");
jQuery(innerDiv2).addClass("calcform_inner");

theForm.action = "";
theForm.method = "post";

/**************************************************
* Build and insert the actual interest form
***************************************************/

theForm.appendChild(innerDiv1);
innerDiv1.appendChild(label1);
innerDiv1.appendChild(input1);
innerDiv1.appendChild(break1);
innerDiv1.appendChild(label2);
innerDiv1.appendChild(input2);
innerDiv1.appendChild(break2);

theForm.appendChild(innerDiv2);
innerDiv2.appendChild(label3);
innerDiv2.appendChild(input3);
innerDiv2.appendChild(break3);
innerDiv2.appendChild(label4);
innerDiv2.appendChild(input4);
innerDiv2.appendChild(break4);
theForm.appendChild(clearfix);
theForm.appendChild(errbox);
theForm.appendChild(submit);

formDiv.appendChild(theForm);
formDiv.id = "plotform";

dom.getElementById("ak-blog-post")
	.insertBefore(formDiv, dom.getElementById("primary"));


/**************************************************
* Style the interest form
***************************************************/

d3.select("#plotform")
	.style({"margin-bottom": "30px","max-width":"800px"});
d3.selectAll("#plotform input")
	.style({"margin": "0 10px 10px","border":"2px solid green"});
d3.selectAll(".calcform_inner")
	.style({"float":"left","width":"45%","margin-left":"2%","min-width":"360px","max-width":"500px","text-align":"right"});
d3.select(submit)
	.style({"width":"100%","max-width":"800px"});
d3.select(clearfix)
	.style({"clear":"both"});


/**************************************************
* Setup the Figure
***************************************************/
if (window.innerWidth > 820) {
	var vis = d3.select("#figure_container"),
		width = 800,
		height = 300,
		margins = {top: 60, right: 20, bottom: 20, left: 100};
} else if (/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)) {
	var vis = d3.select("#figure_container"),
		width = window.innerWidth - 20,
		height = width * 6/8,
		margins = {top: 60, right: 0, bottom: 10, left: 50};
} else {
	var vis = d3.select("#figure_container"),
		width = window.innerWidth - 20,
		height = width * 6/8,
		margins = {top: 60, right: 0, bottom: 20, left: 70};
}


vis.attr("width",width).attr("height",height);

/* The Default Parameters */
var nyears = 30,
	int_rate = 7,
	princ = 5000,
	contr = 400;


/**************************************************
* Setup functions
***************************************************/
// This is for formatting money with commas
// Sourced from: http://stackoverflow.com/questions/149055/how-can-i-format-numbers-as-money-in-javascript
Number.prototype.formatMoney = function(c, d, t){
var n = this, 
    c = isNaN(c = Math.abs(c)) ? 2 : c, 
    d = d == undefined ? "." : d, 
    t = t == undefined ? "," : t, 
    s = n < 0 ? "-" : "", 
    i = parseInt(n = Math.abs(+n || 0).toFixed(c)) + "", 
    j = (j = i.length) > 3 ? j % 3 : 0;
   return s + (j ? i.substr(0, j) + t : "") + i.substr(j).replace(/(\d{3})(?=\d)/g, "$1" + t) + (c ? d + Math.abs(n - i).toFixed(c).slice(2) : "");
 };

/********************************************************
*	The actual calculation of interest on investment with
*	regular contributions of a static amount.
********************************************************/
var interest = function(principal, rate, years, contr) {
	var N_comp = 12., // Compounded monthly
		rate = rate/100., // into percent
		N = (years*N_comp), // total number of compounding periods
		total = [principal/1000]; // array for holding totals for every month

	for (ii = 0; ii < N; ii++) { // the calculation
		var newtot = (Math.pow(1+rate/N_comp, ii+1))*principal + contr*(Math.pow(1 + rate/N_comp,ii+1)-1.)/(rate/N_comp);
		total.push(newtot/1000);
	};
	return total
};

/******************************************************************
* 	Pushing data generated by interest function into X and Y coordinates
* 	that can be used for a line in D3
******************************************************************/
var interestLine = function(princ, rate, nyears, contr) {
	var totals = interest(princ, rate, nyears, contr), // Get the data
		nsteps = nyears * 12, // total number of steps
		lineData = [] // array to hold data values;

	for (var ii = 0; ii < nsteps + 1; ii++) { // push formatted data into array
		lineData.push({x: ii, y: totals[ii], title: "Month: " + ii + "; Amount: $" + (totals[ii] * 1000).formatMoney(2)});
	};
	return lineData;
};

lineData = interestLine(princ, int_rate, nyears, contr);

/*********************************************************************
*	Set the scale and range of the axes. Remember that the horizontal
*	axis starts at the left side, so start that svg range at the left
*	margin. Have it go not the full width, but up to the right margin
**********************************************************************/
  xRange = d3.scale.linear() // linear d3 scale to map valued data onto SVG pixel space
    .range([margins.left, width - margins.right]) // pixel space; start at left margin, end right margin
    .domain([d3.min(lineData, function(d){ // value space
      return d.x;
    }), d3.max(lineData, function(d) { 
      return d.x;
    })]),

// The vertical axis starts at the top and goes down
  yRange = d3.scale.linear() 
    .range([height - margins.top, margins.bottom]) // pixel space; start at the bottom, draw up
    .domain([0, d3.max(lineData, function(d) {
      return d.y;
    })]),

  xAxis = d3.svg.axis() // draw axis based on the given scale
    .scale(xRange)
    .tickSize(5), // So every 5 increments we should get a major tick mark

  yAxis = d3.svg.axis()
    .scale(yRange)
    .tickSize(5)
    .ticks(6) // specify number of ticks to have at all times
    .orient('left'), // Want to put this on the left since it's the y-axis

// Place the axes on the figure
vis.append('svg:g')
	.attr('class', 'axis--x')
	.attr('transform', 'translate(0,' + (height - margins.top) + ')')
	.call(xAxis)
	.style({"fill":"none","stroke":"black","stroke-width":"1"});

vis.append('svg:g')
	.attr('class', 'axis--y')
	.attr('transform', 'translate('+ (margins.left) +', 0)')
	.call(yAxis)
	.style({"fill":"none","stroke":"black","stroke-width":"1"});

//// Place labels on the axes
// Y-axis
vis.append("text")
	.attr("id", "y-title")
	.attr("transform","rotate(270)")
	.attr("x", (-height/2))
	.attr("y", (margins.left/3))
	.attr("text-anchor", "middle")
	.text("Amount (Thousands $)");

// X-axis
vis.append("text")
	.attr("id", "x-title")
	.attr("x", (width/2 + margins.right))
	.attr("y", (height - (margins.top)/3))
	.attr("text-anchor", "middle")
	.text("Months after Initial Investment")

// Create the line generator function
var lineFunc = d3.svg.line()
	.x(function(d) {
		return xRange(d.x);
	})
	.y(function(d) {
		return yRange(d.y);
	})
	.interpolate('basis');

var plotLine = function(lineData, color){ // function for plotting any line
	vis.append('svg:path')
		.attr('d', lineFunc(lineData)) // This is where you add the data
		.attr('stroke', color) // line color
		.attr('stroke-width', 2) // line width
		.attr('class','interest_line')
		.attr('fill', 'none');
};

// Add the line to the doc
plotThis = plotLine(lineData, "green");

/****************************************
*	If the parameters change and changes are
*	submitted, redraw the figure with a
*	new line and new axes
***************************************/
jQuery("button#submit").on('click', function(e) {
	e.preventDefault(); // hitting submit shouldn't take you to a new page

	var	numberCheck = function(value){ // check to make sure input values are valid
			if (eval(value) < 1e20 && eval(value) >= 0) {
				return eval(value);
			} else {
				return false;
			}
		};

	var money_in = numberCheck(jQuery("#money_input").val()), // check all inputs
		rate_in = numberCheck(jQuery("#rate_input").val()),
		time_in = numberCheck(jQuery("#time_input").val()),
		contr_in = numberCheck(jQuery("#monthly_input").val());

	
	
	// if any input is wrong, throw up error box. Otherwise, go on and redraw.
	if (money_in !== false && rate_in !== false && time_in !== false && contr_in !== false) {

		jQuery(".interest_line").remove();
		d3.select(errbox).style({"display":"none"});

		lineData = interestLine(money_in, rate_in, time_in, contr_in);

		// Replot the axes
		jQuery(".axis--x").remove();
		jQuery(".axis--y").remove();

		xRange = d3.scale.linear()
		    .range([margins.left, width - margins.right])
		    .domain([0, d3.max(lineData, function(d) {
		      return d.x;
		    })]);

		yRange = d3.scale.linear()
		    .range([height - margins.top, margins.bottom])
		    .domain([0, d3.max(lineData, function(d) {
		      return d.y;
		    })]);

		xAxis = d3.svg.axis()
			.scale(xRange)
			.tickSize(5)
			.tickSubdivide(20);

		yAxis = d3.svg.axis()
			.scale(yRange)
			.tickSize(5)
			.ticks(6)
			.tickSubdivide(20)
			.orient('left'); // Want to put this on the left since it's the y-axis

		vis.append('svg:g')
			.attr('class', 'axis--x')
			.attr('transform', 'translate(0,' + (height - margins.top) + ')')
			.call(xAxis)
			.style({"fill":"none","stroke":"black","stroke-width":"1"});

		vis.append('svg:g')
			.attr('class', 'axis--y')
			.attr('transform', 'translate('+ (margins.left) +', 0)')
			.call(yAxis)
			.style({"fill":"none","stroke":"black","stroke-width":"1"});

		plotThis = plotLine(lineData, "green");
	} else {
		d3.select(errbox)
			.style({"display":"block", 
				"color": "white",
				"text-align": "center",
				"font-weight": "600",
				"background": "red",
				"margin-bottom": "5px",
				"padding": "2px"});

		errbox.innerHTML = "Input fields need numbers";
		console.log("Something was wrong");
	}

});

// ====================
// Want an information box for
// the values at a given mouse coordinate
// ====================

var thinbox = vis.append("rect") // traces the X-axis only
	.attr("x", margins.left)
	.attr("y", 0)
	.attr("width", 1)
	.attr("height", height - margins.bottom)
	.attr("fill", "teal")
	.attr("opacity","0");

var emptycirc = vis.append("circle") // pinpoints where on graph line we are
	.attr("cx", margins.left)
	.attr("cy", 0)
	.attr("r", 10)
	.attr("fill", "none")
	.attr("stroke", "blue")
	.attr("opacity","0");

var infobox = dom.createElement("div"); // tells you what values are at a given x coord
infobox.id = "infobox";
d3.select(infobox)
	.style({"max-width":"800px",
			"text-align":"center",
			"margin-bottom":"20px"});

infobox.innerHTML = "";

dom.getElementById("ak-blog-post")
	.insertBefore(infobox, dom.getElementById("plotform"));

var months2years = function(nmonths){
	var nyears = Math.floor(nmonths/12),
		months = nmonths - nyears*12;
	if (nyears < 1) {
		if (nmonths === 1) {
			return nmonths + " Month";
		} else {
		return nmonths + " Months"; 
		}

	} else if (nyears === 1){
		if (months === 1) {
			return nyears + " Year and " + months + " Month";
		} else if (months === 0){
			return nyears + " Year";
		} else {
			return nyears + " Year and " + months + " Months";
		}

	} else {
		if (months === 1) {
			return nyears + " Years and " + months + " Month";
		} else if (months === 0){
			return nyears + " Years";
		} else {
			return nyears + " Years and " + months + " Months";
		}
	}
}

vis.on("mousemove", function(){
	position = d3.mouse(this);
	xpos = position[0];
	ypos = position[1];
	monthround = Math.round(xRange.invert(xpos));
	money_out = lineData[monthround].y * 1000;
	infobox.innerHTML = "Time: " + months2years(monthround) + "<br>Balance: $" + money_out.formatMoney(2);
	thinbox.attr("x",xpos).attr("opacity", "1");

	emptycirc.attr("cx",xpos).attr("cy", yRange(lineData[monthround].y)).attr("opacity","1");
});

vis.on("mouseout", function(){
	thinbox.attr("opacity", "0");
	emptycirc.attr("opacity", "0");
});

});

