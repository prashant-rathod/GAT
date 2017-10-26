function drawSVG(systemMeasures) {
   var toDraw = ["Baseline","Resilience","Robustness"]
   for (measure in toDraw) {
      //Make an SVG Container
      var svgContainer = d3.select("#resilienceInfo").append("svg").attr("id",toDraw[measure])
                                                                   .attr("style","width:80%;height:auto")
          width = svgContainer.node().getBoundingClientRect().width * .9
          height = width/15
          defaultY = height
          text = {}
          values = []
          lowerLabel = svgContainer.append("text").html("Low "+toDraw[measure])
              .attr("x",0)
              .attr("y","12px")
              .attr("fill","white")
              .attr("style","font-size:12px")
          higherLabel = svgContainer.append("text").html("High "+toDraw[measure])
              .attr("x",width*.9)
              .attr("y","12px")
              .attr("fill","white")
              .attr("style","font-size:12px")
          rect = svgContainer.append("rect").attr("width",width)
              .attr("height",String(height)+"px")
              .attr("y",defaultY)
              .attr("fill","url(#gradient)")
      for ( cluster in systemMeasures[toDraw[measure]] ) {
         var cluster_safe = cluster.replace("'","").replace(" ","")
         text.cluster = {}
         text.cluster.line = svgContainer.append("rect").attr("width",width/200)
             .attr("height",height*1.5)
             .attr("x",0)
             .attr("y",defaultY-height*.25)
             .attr("fill","white")
         text.cluster.content = svgContainer.append("text").html(cluster)
             .attr("x",0)
             .attr("y",height*2+defaultY)
             .attr("fill","white")
             .attr("style","font-size:12px")
             .attr("class",cluster_safe+" content")
             .attr("id",cluster_safe+"_"+measure)
         $("#"+cluster_safe+"_"+measure)
            .mouseover(function() {
                console.log("mouseover");
               var clusterClass = this.classList[0]
               d3.selectAll("text").transition().duration(1000).attr("opacity",function() {
                  return ( $.inArray(clusterClass, this.classList) ) ? .25 : 1.0;
               });
               d3.selectAll(".value").transition().duration(500).attr("opacity",function() {
                  return ($.inArray(clusterClass, this.classList) ) ? 0 : 1.0;
               })
            })
            .mouseout(function() {
               d3.selectAll("text").transition().duration(2000).attr("opacity",1.0)
               d3.selectAll(".value").transition().duration(2000).attr("opacity",0)
            })
         var percentile = systemMeasures[toDraw[measure]][cluster][0]
         var x = width * percentile / 100
         values.push(x)
         var c = 1
         var y = 0
         for (i in values) {
            if (x == values[i]) {
               c += 1; // Used to determine y position
            }
            if (c > 5) {
               c = 2;
               y += 1;
            }
         }
         var t = 2000
         var contentWidth = text.cluster.content.node().getBBox().width / width * 100
         var contentHeight = text.cluster.content.node().getBBox().height / svgContainer.node().getBoundingClientRect().height * 100
         text.cluster.line.transition().duration(t).attr("x",x)
         text.cluster.content.transition().duration(t).attr("x",x-contentWidth*2+contentWidth*y*5)
                                                     .attr("y",contentHeight*c*2+defaultY+height/2)
         text.cluster.value = svgContainer.append("text").html(systemMeasures[toDraw[measure]][cluster][0])
             .attr("opacity",0)
             .attr("x",x-contentWidth/2)
             .attr("y",defaultY-height*.5)
             .attr("style","font-size:12px")
             .attr("class",cluster_safe+" value")
             .style("font-weight","bold")
             .style("fill","rgb("+Math.round((1-percentile/100)*255)+","+0+","+Math.round(percentile/100*255)+")")
      }
   }
}
