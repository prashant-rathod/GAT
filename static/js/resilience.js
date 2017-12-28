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
                            top: 20,
                            right: 100,
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
        vis.append('svg:path')
            .attr('d', lineGen(trace))
            .attr('stroke', colors[i])
            .attr('stroke-width', 2)
            .attr('fill', 'none');
        vis.append("text")
            .attr("transform", "translate(" + (WIDTH-50) + "," + (20*(1+i)) + ")")
            .attr("dy", ".35em")
            .attr("text-anchor", "start")
            .style("fill", colors[i])
            .text(cluster);
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
        vis.append("text")
            .attr("transform", "translate(" + (WIDTH-MARGINS.right) + "," + reScaleY(systemMeasures["Resilience"][cluster]) + ")")
            .attr("dy", ".35em")
            .attr("text-anchor", "start")
            .style("fill", colors[i])
            .text("Average");
        i++;
    }
}
