module.exports.main = function () {
 /* 
  var createGraph = require('ngraph.graph');
  var graph = createGraph();
  graph.addNode("test1", "test1");
  graph.addNode("test2", "test2");
  graph.addNode("test3", "test3");
  graph.addNode("test4", "test4");
  graph.addLink("test1", "test2");
  graph.addLink("test1", "test3");
  graph.addLink("test1", "test4");
  
  graph.addLink("test2", "test3");
  graph.addLink("test2", "test4");

  graph.addLink("test3", "test4");
  //graph.getLink("test3", "test4").color = 0xFF0000;
  // And render it
  var nthree = require('ngraph.three');
  var graphics = nthree(graph);

  graphics.run(); // begin animation loop
  //graph.getLink("test3", "test4").color = 0xFF0000;
  //console.log(graph.getLink("test3", "test4"));
  var nodeUI = graphics.getNode("test1");
  nodeUI.color = 0xFF0000; // update node color
  nodeUI.size = 30; // update size
*/
  var createGraph = require('ngraph.graph');
  var graph = createGraph();
  var threeGraphics = require('../../')(graph);

  var THREE = threeGraphics.THREE;

  // tell graphics we want custom UI
  threeGraphics.createNodeUI(function () {
    var size = Math.random() * 10 + 1;
    var nodeGeometry = new THREE.BoxGeometry(size, size, size);
    var nodeMaterial = new THREE.MeshBasicMaterial({ color: getNiceColor() });
    return new THREE.Mesh(nodeGeometry, nodeMaterial);
  }).createLinkUI(function() {
    var linkGeometry = new THREE.Geometry();
    // we don't care about position here. linkRenderer will update it
    linkGeometry.vertices.push(new THREE.Vector3(0, 0, 0));
    linkGeometry.vertices.push(new THREE.Vector3(0, 0, 0));

    var linkMaterial = new THREE.LineBasicMaterial({ color: getNiceColor() });
    return new THREE.Line(linkGeometry, linkMaterial);
  });
  graph.addNode("test1", "test1");
  graph.addNode("test2", "test2");
  graph.addNode("test3", "test3");
  graph.addNode("test4", "test4");
  graph.addLink("test1", "test2");
  graph.addLink("test1", "test3");
  graph.addLink("test1", "test4");
  
  graph.addLink("test2", "test3");
  graph.addLink("test2", "test4");

  graph.addLink("test3", "test4");
  var div = d3.select("body").append("div")
                            .attr("class", "tooltip")
                            .style("opacity", 0);
  var eventify = require('ngraph.events');
  eventify(graph.getNode("test1"));
  graph.getNode("test1").on("mouseover", function(){div.transition().duration(200).style("opacity", .9);
                                div .html("<p>" + node.data + "</p>").style("top", (d3.event.pageY - 50) + "px").style("left", (d3.event.pageX ) + "px");})
                            .on("mousemove", function(){div .html("<p>" + node.data + "</p>").style("top", (d3.event.pageY - 50) + "px").style("left", (d3.event.pageX ) + "px");})
                            .on("mouseout", function(){div.transition().duration(500).style("opacity", 0);});
  /*graph.forEachNode(function (node){
    node.on("mouseover", function(){div.transition().duration(200).style("opacity", .9);
                                div .html("<p>" + node.data + "</p>").style("top", (d3.event.pageY - 50) + "px").style("left", (d3.event.pageX ) + "px");})
                            .on("mousemove", function(){div .html("<p>" + node.data + "</p>").style("top", (d3.event.pageY - 50) + "px").style("left", (d3.event.pageX ) + "px");})
                            .on("mouseout", function(){div.transition().duration(500).style("opacity", 0);});
  });*/
  //threeGraphics.camera.position.z = 1000;
  // begin rendering loop:
  threeGraphics.run();
};

var niceColors = [
 0x1f77b4, 0xaec7e8,
 0xff7f0e, 0xffbb78,
 0x2ca02c, 0x98df8a,
 0xd62728, 0xff9896,
 0x9467bd, 0xc5b0d5,
 0x8c564b, 0xc49c94,
 0xe377c2, 0xf7b6d2,
 0x7f7f7f, 0xc7c7c7,
 0xbcbd22, 0xdbdb8d,
 0x17becf, 0x9edae5
];

function getNiceColor() {
  return niceColors[(Math.random() * niceColors.length)|0];
}

