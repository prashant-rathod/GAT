function drawSVG(systemMeasures) {
    var inf = Math.pow(10, 1000);
    var domain = {min: 0, max: 0}
    var range = {min: inf, max: -inf}
    for (cluster in systemMeasures["Trace"]) {
        trace = systemMeasures["Trace"][cluster]
        domain.max = trace.length > domain.max ? trace.length : domain.max;
        for (var i=0; i<trace.length; i++) {
            var val = trace[i];
            if (val < range.min) {
                range.min = val;
            }
            if (val > range.max) {
                range.max = val;
            }
            trace[i] = {
                x: i,
                y: val
            }
        }
    }
    var svgContainer = d3.select("#resilienceInfo").append("svg").attr("style","width:570px;height:540px")
                                                                 .attr("id","vis")
                                                                 .style("background-color","white")
    var vis = d3.select("#vis"),
                        MARGINS = {
                            top: 0,
                            right: 200,
                            bottom: 20,
                            left: 50
                        },
                        WIDTH = 500,
                        HEIGHT = 500,
                        xScale = d3.scaleLinear().rangeRound([MARGINS.left, WIDTH - MARGINS.right]).domain([domain.min, domain.max]),
                        yScale = d3.scaleLinear().rangeRound([HEIGHT - MARGINS.top, MARGINS.bottom]).domain([-1, 1]),
                        xAxis = d3.axisBottom()
                        .scale(xScale),
                        yAxis = d3.axisLeft()
                        .scale(yScale)
    vis.append("g")
        .attr("class", "x axis")
        .attr("transform", "translate(0," + (HEIGHT / 2) + ")")
        .call(xAxis);
    vis.append("g")
        .attr("class", "y axis")
        .attr("transform", "translate(" + (MARGINS.left) + ",0)")
        .call(yAxis);
    var reScaleY = function(d) {
        var scaleCoef = 2/(range.max-range.min);
        var diff = d - range.min;
        return yScale(scaleCoef * diff - 1);
    }
    // gridlines
    for (var i=-1; i<=1; i+=0.1) {
      vis.append('svg:path')
                .attr('d', "M"+MARGINS.left+" "+yScale(i)+"H"+WIDTH-MARGINS.right)
                .attr('stroke', "gray")
                .attr('stroke-width', 1)
                .attr('fill', 'none');
    }
    // axis labels
    vis.append("text")
                .attr("transform", "translate(" + (10) + "," + yScale(0.4) + ")rotate(-90)")
                .attr("dy", ".50em")
                .attr("text-anchor", "start")
                .style("fill", "black")
                .text("Resilience Measure");
    vis.append("text")
                .attr("transform", "translate(" + (10) + "," + yScale(.1) + ")")
                .attr("dy", ".50em")
                .attr("text-anchor", "start")
                .style("fill", "black")
                .text("Time");

    //drawing the lines
    var lineGen = d3.line()
        .x(function(d) {
            return xScale(d.x);
        })
        .y(function(d) {
            return reScaleY(d.y);
        })
    var i = 0;
    var colors = ["green","red","blue","yellow"];
    for (cluster in systemMeasures["Trace"]) {
        trace = systemMeasures["Trace"][cluster]
        // the trace
        vis.append('svg:path')
            .attr('d', lineGen(trace))
            .attr('stroke', colors[i])
            .attr('stroke-width', 2)
            .attr('fill', 'none')
            .transition()
            .duration(3000)
        // the label
        vis.append("text")
            .attr("transform", "translate(" + (WIDTH-MARGINS.right/3) + "," + (20*(1+i)) + ")")
            .attr("dy", ".35em")
            .attr("text-anchor", "start")
            .style("fill", colors[i])
            .text(cluster);
        // creating a straight line for the average
        var average = [];
        for (var k=0; k<trace.length; k++) {
            average[k] = {
                x: k,
                y: systemMeasures["Resilience"][cluster]
            }
        }
        vis.append('svg:path')
            .attr('d', lineGen(average))
            .attr('stroke', colors[i])
            .attr('stroke-width', 2)
            .attr('fill', 'none')
            .style('stroke-dasharray',("2,2"));
        // label for average lines
//        vis.append("text")
//            .attr("transform", "translate(" + (WIDTH-MARGINS.right) + "," + reScaleY(systemMeasures["Resilience"][cluster]) + ")")
//            .attr("dy", ".35em")
//            .attr("text-anchor", "start")
//            .style("fill", colors[i])
//            .text("Average");
        i++;
    }

    // Draw curly bracket labels
    //returns path string d for <path d="This string">
    //a curly brace between x1,y1 and x2,y2, w pixels wide
    //and q factor, .5 is normal, higher q = more expressive bracket
    function makeCurlyBrace(x1,y1,x2,y2,w,q)
    {
        //Calculate unit vector
        var dx = x1-x2;
        var dy = y1-y2;
        var len = Math.sqrt(dx*dx + dy*dy);
        dx = dx / len;
        dy = dy / len;

        //Calculate Control Points of path,
        var qx1 = x1 + q*w*dy;
        var qy1 = y1 - q*w*dx;
        var qx2 = (x1 - .25*len*dx) + (1-q)*w*dy;
        var qy2 = (y1 - .25*len*dy) - (1-q)*w*dx;
        var tx1 = (x1 -  .5*len*dx) + w*dy;
        var ty1 = (y1 -  .5*len*dy) - w*dx;
        var qx3 = x2 + q*w*dy;
        var qy3 = y2 - q*w*dx;
        var qx4 = (x1 - .75*len*dx) + (1-q)*w*dy;
        var qy4 = (y1 - .75*len*dy) - (1-q)*w*dx;

    return ( "M " +  x1 + " " +  y1 +
            " Q " + qx1 + " " + qy1 + " " + qx2 + " " + qy2 +
            " T " + tx1 + " " + ty1 +
            " M " +  x2 + " " +  y2 +
            " Q " + qx3 + " " + qy3 + " " + qx4 + " " + qy4 +
            " T " + tx1 + " " + ty1 );
    }
    function makeZone(min,max,label) {
        var bracketX = WIDTH-MARGINS.right*.9;
        vis.append('svg:path')
                .attr('d', makeCurlyBrace(bracketX,yScale(min),bracketX,yScale(max),20,.7))
                .attr('stroke', "black")
                .attr('stroke-width', 2)
                .attr('fill', 'none');
        vis.append("text")
                .attr("transform", "translate(" + (bracketX+30) + "," + yScale((max+min)/2) + ")")
                .attr("dy", ".35em")
                .attr("text-anchor", "start")
                .style("fill", "black")
                .text(label);
    }
    makeZone(-1,-.7,"Fragile");
    makeZone(-1,-.3,"Resilient");
    makeZone(-.3,.3,"Coping");
    makeZone(.3,.7,"Robust");
    makeZone(.7,1,"Antifragile");
}
