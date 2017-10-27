//---------------------
/*
Jgraph UI Scripts for Hermes 2.0
Author: Ryan Steed, 21 Jun 2017
*/
//---------------------

// Toggles for tab display in info window
attributesToggle = function() {
  document.getElementById('measureInfo').style.display='none';
  document.getElementById('attributes').style.display='inline-block';
  document.getElementById('propInfo').style.display='none';
  tablinks = document.getElementsByClassName("tablinks");
  for (i = 0; i < tablinks.length; i++) {
    tablinks[i].className = tablinks[i].className.replace(" active", "");
  }
  event.currentTarget.className += " active";
}
measuresToggle = function() {
  document.getElementById('measureInfo').style.display='inline-block';
  document.getElementById('attributes').style.display='none';
  document.getElementById('propInfo').style.display='none';
  tablinks = document.getElementsByClassName("tablinks");
  for (i = 0; i < tablinks.length; i++) {
    tablinks[i].className = tablinks[i].className.replace(" active", "");
  }
  event.currentTarget.className += " active";
}
propToggle = function() {
  document.getElementById('propInfo').style.display='inline-block';
  document.getElementById('measureInfo').style.display='none';
  document.getElementById('attributes').style.display='none';
  tablinks = document.getElementsByClassName("tablinks");
  for (i = 0; i < tablinks.length; i++) {
    tablinks[i].className = tablinks[i].className.replace(" active", "");
  }
  event.currentTarget.className += " active";
}

// window minimization and maximization functions
minimizeTabs = function() {
  $('#nodeInfo').css('display','none');
  $('.tab').css('display','none');
}
maximizeTabs = function() {
  $('#nodeInfo').css('display','inline-block');
  $('.tab').css('display','inline-block');
}

// For editing attributes (WIP)
handleEditButton = function() {
  toggleEditWindow();
  $("#editAttributeInfo").empty();
  $("#editAttributeInfo").append("<div class='rightIcon' onclick='toggleEditWindow()'><i class='fa fa-window-close'></i></div>")
  for (var feature in currentNodeDict['attributes']) {
    if (feature != 'name') {
      $("#editAttributeInfo").append('<span>'+feature+': </span><input class="editInputs"id="'+feature+'" name="'+feature+'" value="'+currentNodeDict['attributes'][feature]+'"></input><br />');
    }
  }
  $("#editAttributeInfo").append('<input id="editSubmitButton" type="submit" name="editSubmitButton" value="Submit" onclick="handleEditSubmit(currentNodeDict)" />')
};

toggleEditWindow = function() {
  $("#attributeInfo").toggleClass("closed")
  $("#editAttributeInfo").toggleClass("closed")
}

// Add node window CSS transition support
showAddNodeWindow = function() {
  $("#toolbar").toggleClass("closed")
  $("#addNodeWindow").toggleClass("closed")
  attributeFlag = !attributeFlag;
}

// Add node window CSS transition support
showAddEventWindow = function() {
  $("#toolbar").toggleClass("closed")
  $("#addEventWindow").toggleClass("closed")
  attributeFlag = !attributeFlag;
}

// UI interactions for addNode form data
// 29 Jun 2017 Ryan Steed
counter = 0
handleAddAttributeClick = function() {
  $("#addAttrButton"+counter).toggleClass("fa-plus-circle")
  $("#addAttrButton"+counter).toggleClass("fa-minus-circle")
  $("#addAttrButton"+counter).attr("onclick","removeAttr("+counter+")")
  $("#attribute"+counter).attr("readonly","true")
  counter += 1
  $("#addAttrTarget").append('<div><i id="addAttrButton'+counter+'" class="fa fa-plus-circle" onclick="handleAddAttributeClick()"></i><input class="attrInput" type="text" id="attribute'+counter+'" name="attribute'+counter+'" placeholder="Attribute" />:<input type="text" class="valInput" id="value'+counter+'" name="value'+counter+'" placeholder="Value" /><input type="text" class="wInput" id="weight'+counter+'" name="weight'+counter+'" placeholder="Weight" /></div>')
}
removeAttr = function(id) {
  console.log("removing..")
  var id = $('#addAttrButton'+id)
  id.closest('div').remove();
};
counter2 = 0;
handleAddLinkClick = function(nodeName) {
  $("#addLinkTarget").append('<div><i id="minusLinkButton'+counter2+'" class="fa fa-minus-circle" onclick="removeLink('+counter2+')"></i> <input type="text" id="link'+counter2+'" name="link'+counter2+'" readonly/></div>')
  $('#link'+counter2).val(nodeName)
  counter2 += 1
}
removeLink = function(id) {
  console.log("removing..")
  $('#link'+id).closest('div').remove();
};

// Placeholder message during resilience calculation
handleResilienceClick = function() {
    $("#resilience").attr("value","Calculating Resilience...")
                    .attr("data-original-title","Resilience is being calculated. This is a heavy process and may require 1-2 minutes for completion.")
}

// Placeholder message during ERGM run
handleAddClick = function() {
    showAddNodeWindow();
    $("#add").attr("value","Adding Nodes...")
             .attr("data-original-title","Currently conducting DRAG analysis (1-2 min).")
}

// Placeholder message during influence detection
handleCliqueClick = function() {
    $("#cliques").attr("value","Detecting Communities...")
             .attr("data-original-title","Currently conducting community detection (30-90s).")
}

// Code for tooltips
$(document).ready(function(){
    $('[data-toggle="tooltip"]').tooltip();
});
