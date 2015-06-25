/*  
    Onno Hartveldt
    10972935

    visualisation:
    "Wie zijn de nakomelingen van een wetenschappelijke publicatie?"

    source: http://bl.ocks.org/sjengle/5431779
*/

/* GLOBALS */

"use strict";

var width  = 1010;           // width of svg image
var height = 460;           // height of svg image
var margin = 20;            // amount of margin around plot area
var pad = margin / 2;       // actual padding amount
var radius = 4;             // fixed node radius
var yfixed = pad + radius;  // y position for all nodes
var xfixed = width / 2;


var yscale = d3.scale.linear()
    .range([radius, height - margin - radius]);

// scale to generate radians (just for lower-half of circle)
var radians = d3.scale.linear()
    .range([Math.PI / 180, Math.PI]);

// path generator for arcs (uses polar coordinates)
var arc = d3.svg.line.radial()
    .interpolate("basis")
    .tension(0)
    .angle(function(d) { return radians(d); });

//Toggle stores whether the highlighting is on
var toggle = 0;


/* MAIN DRAW METHOD */

// Draws an arc diagram for the provided undirected graph
function arcDiagram(graph) {
    // create svg image
    var svg  = d3.select("body")
        .append("svg")
        .attr("id", "arc")
        .attr("width", width)
        .attr("height", height);

    // draw border around svg image
    svg.append("rect")
        .attr("class", "outline")
        .attr("width", width)
        .attr("height", height);

    // create plot area within svg image
    var plot = svg.append("g")
        .attr("id", "plot")
        .attr("transform", "translate(" + pad + ", " + pad + ")");

    // fix graph links to map to objects instead of indices
    graph.links.forEach(function(d, i) {
        d.source = isNaN(d.source) ? d.source : graph.nodes[d.source];
        d.target = isNaN(d.target) ? d.target : graph.nodes[d.target];
    });

    graph = graph

    d3.select("input").on("change", change);

    // must be done AFTER links are fixed
    linearLayout(graph.nodes);

    // draw links first, so nodes appear on top
    drawLinks(graph.links);

    // draw nodes last
    drawNodes(graph);
}

/* STATIC FUNCTIONS*/

// Layout nodes linearly, sorted by...
function linearLayout(nodes) {
    // sort nodes by group
    nodes.sort(function(a, b) {
        return a.name.length - b.name.length;   //by citations 
    });

    // used to scale node index to x position
    var xscale = d3.scale.linear()
        .domain([0, nodes.length - 1])
        .range([radius, width - margin - radius]);

    yscale.domain([0, nodes.length - 1]);


    // calculate pixel location for each node
    nodes.forEach(function(d, i) {
        d.x = xfixed;       // vertikale weergave
        d.y = yscale(i);    //
    });
}


// Draws nodes on plot
function drawNodes(graph) {
    // used to assign nodes color by group
    
    var tmp = d3.select("#plot").selectAll(".node")
        .data(graph.nodes)
        .enter()
        .append("g")
        .attr("class", "node")
        .style("stroke", function(d) {return d.generation == 1 ? "#000000" : "#ffffff"; })
        .on("click", function(p, i) { makeImportant(d3.select(this)); })

    tmp.append("circle")
        .attr("class", "circle" )
        .attr("id", function(d, i) { return d.name; })
        .attr("cx", function(d, i) { return d.x; })
        .attr("cy", function(d, i) { return d.y; })
        .attr("r",  function(d, i) { return radius; })
        .attr("toggle", 0)
        .style("fill", "#993404") 
        .on("mouseover", function(d, i) { addTooltip(d3.select(this)); })
        .on("mouseout",  function(d, i) { d3.select("#tooltip").remove(); })
        .on("dblclick", function(p, i){ highLight(graph, i); });

    tmp.append("text")
        .attr("class", "text")
        .text(function(d, i) { return d.name; })
        .attr("x", function(d, i) { return d.x - radius; } )
        .attr("y", function(d, i) { return d.y + radius / 2; })
        .attr("text-anchor", "end")
        .attr("dy", 0)
        .attr("class", "important")
        .style("visibility", "hidden")        
}


// Draws arcs for each link on plot
function drawLinks(links) {

    // add links
    d3.select("#plot").selectAll(".link")
        .data(links)
        .enter()
        .append("path")
        .attr("class", "link")
        .attr("transform", function(d, i) {
            // arc will always be drawn around (0, 0)
            // shift so (0, 0) will be between source and target
            var xshift = xfixed;
            var yshift = d.source.y + (d.target.y - d.source.y) / 2;
            return "translate(" + xshift + ", " + yshift + ")";
        })
        .attr("d", function(d, i) {
            // get y distance between source and target
            var ydist = Math.abs(d.source.y - d.target.y);

            // set arc radius based on x distance
            arc.radius(ydist / 2);

            // want to generate 1/3 as many points per pixel in y direction
            var points = d3.range(0, Math.ceil(ydist / 3));

            // set radian scale domain
            radians.domain([0, points.length - 1]);

            // return path for arc
            return arc(points);
        });
}


/* DYNAMIC FUNCTIONS */

// Generates a tooltip for a SVG circle element based on its ID
function addTooltip(node) {
    var x = parseFloat(node.attr("cx"));
    var y = parseFloat(node.attr("cy"));
    var r = parseFloat(node.attr("r"));
    var text = node.attr("id");


    var tooltip = d3.select("#plot")
        .append("text")
        .text(text)
        .attr("x", x - r)
        .attr("y", y + r / 2)
        .attr("dy", r)
        .attr("id", "tooltip")
        .attr("text-anchor", "end")
        .attr("dy", 0);
}


// Lowers the opacity of the phericial nodes and links of the selection
function highLight(graph, i) {
    // Source: http://www.coppelia.io/2014/07/an-a-to-z-of-extra-features-for-the-d3-force-layout/ 

    //This function looks up whether a pair are neighbours
    function neighboring(a, b) {
        return linkedByYPosition[a.y + "," + b.y];
    }

    //Create an array logging what is connected to what
    var linkedByYPosition = {};

    d3.selectAll(".node").each(function (d) {
        linkedByYPosition[d.y + "," + d.y] = 1;
    });

    d3.selectAll(".link").each(function (d) {
        linkedByYPosition[d.source.y + "," + d.target.y] = 1;
    });

    if (toggle == 0) {
        //Reduce the opacity of all but the neighbouring nodes
        var d = graph.nodes[i];

        d3.selectAll(".node").each( function(a) {
            d3.select(this).style("opacity", function (o) {
                return neighboring(d, o) | neighboring(o, d) ? 1 : 0.3; });
        }); 

        d3.selectAll(".link").each( function(a) {
            d3.select(this).style("opacity", function (o) {
                return d.y == o.source.y | d.y == o.target.y ? 1 : 0.3; });
        });

        //Reduce the op
        toggle = 1; 
    } 
        else {
        //Put them back to opacity=1
        d3.selectAll(".node").style("opacity", 1);
        d3.selectAll(".link").style("opacity", 1);
        toggle = 0; 
    }
}


// makes a select node and its links recognisable
function makeImportant(node){
    
    node.select("circle").attr("toggle", function(o) {
        return node.select("circle").attr("toggle") == 0 ? 1 : 0 ;
    });

    node.each( function(a) {
        node.select(".important").style("visibility", function (o) {
            return node.select("circle").attr("toggle") == 1 ? "visible" : "hidden"; });
    }); 

}


// change linear layout with different sorting
function change() {

    d3.select("#plot").selectAll(".node")
        .sort(this.checked
        ? function(a, b) { return b.generation - a.generation; }
        : function(a, b) { return a.name.length - b.name.length; })
        .each(function(d, i){
            d.y = yscale(i);
        })


    // source: http://bl.ocks.org/mbostock/3885705
    var transition = d3.transition().duration(800),
        delay = function(d, i) { return i * 50; };


    transition.selectAll(".circle")
        .delay(delay)
        .attr("cy", function(d, i) { return yscale(i); });

    transition.selectAll(".important")
        .delay(delay)
        .attr("y", function(d, i) { return yscale(i) + radius / 2; });


    transition.selectAll(".link")
        .delay(delay)
        .attr("transform", function(d, i) {
            // arc will always be drawn around (0, 0)
            // shift so (0, 0) will be between source and target
            var xshift = xfixed;
            var yshift = d.source.y + (d.target.y - d.source.y) / 2;
            return "translate(" + xshift + ", " + yshift + ")";
        })
        .attr("d", function(d, i) {
            // get y distance between source and target
            var ydist = Math.abs(d.source.y - d.target.y);

            // set arc radius based on x distance
            arc.radius(ydist / 2);

            // want to generate 1/3 as many points per pixel in y direction
            var points = d3.range(0, Math.ceil(ydist / 3));

            // set radian scale domain
            radians.domain([0, points.length - 1]);

            // return path for arc
            return arc(points);
        })
}










