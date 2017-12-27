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
        console.log(trace);
    }
    var svgContainer = d3.select("#resilienceInfo").append("svg").attr("style","width:570px;height:540px")
                                                                 .attr("id","vis")
                                                                 .style("background-color","white")
    var vis = d3.select("#vis"),
                        MARGINS = {
                            top: 20,
                            right: 20,
                            bottom: 20,
                            left: 50
                        },
                        WIDTH = 500,
                        HEIGHT = 500,
                        xScale = d3.scaleLinear().rangeRound([MARGINS.left, WIDTH - MARGINS.right]).domain([domain.min, domain.max]),
                        yScale = d3.scaleLinear().rangeRound([HEIGHT - MARGINS.top, MARGINS.bottom]).domain([range.min, range.max]),
                        xAxis = d3.axisBottom()
                        .scale(xScale),
                        yAxis = d3.axisLeft()
                        .scale(yScale)
    vis.append("g")
        .attr("class", "x axis")
        .attr("transform", "translate(0," + (HEIGHT - MARGINS.bottom) + ")")
        .call(xAxis);
    vis.append("g")
        .attr("class", "y axis")
        .attr("transform", "translate(" + (MARGINS.left) + ",0)")
        .call(yAxis);
    var lineGen = d3.line()
        .x(function(d) {
            return xScale(d.x);
        })
        .y(function(d) {
            return yScale(d.y);
        })
    var i = 0;
    var colors = ["green","red","blue","yellow"];
    for (cluster in systemMeasures["Trace"]) {
        trace = systemMeasures["Trace"][cluster]
        vis.append('svg:path')
            .attr('d', lineGen(trace))
            .attr('stroke', colors[i])
            .attr('stroke-width', 2)
            .attr('fill', 'none');
        console.log(systemMeasures["Resilience"])
        var baseline = [];
        for (var k=0; k<trace.length; k++) {
            baseline[k] = {
                x: k,
                y: systemMeasures["Resilience"][cluster]
            }
        }
        vis.append('svg:path')
            .attr('d', lineGen(baseline))
            .attr('stroke', colors[i])
            .attr('stroke-width', 2)
            .attr('fill', 'none')
            .style('stroke-dasharray',("2,2"));
        i++;
    }

}
