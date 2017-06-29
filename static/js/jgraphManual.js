//---------------------
/*
Jgraph UI Scripts for Hermes 2.0
Author: Ryan Steed, 21 Jun 2017
*/
//---------------------

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

minimizeTabs = function() {
  $('#nodeInfo').css('display','none');
  $('.tab').css('display','none');
}
maximizeTabs = function() {
  $('#nodeInfo').css('display','inline-block');
  $('.tab').css('display','inline-block');
}

handleEditButton = function() {
  toggleEditWindow();
  $("#editAttributeInfo").empty();
  $("#editAttributeInfo").append("<div class='centeredIcon' onclick='toggleEditWindow()'><i class='fa fa-window-close'></i></div>")
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

showAddNodeWindow = function() {
  $("#toolbar").toggleClass("closed")
  $("#addNodeWindow").toggleClass("closed")
}
counter = 0
handleAddAttributeClick = function() {
  $("#addAttrButton"+counter).toggleClass("fa-plus-circle")
  $("#addAttrButton"+counter).toggleClass("fa-minus-circle")
  $("#addAttrButton"+counter).toggleClass("minusAttrButton")
  $("#addAttrButton"+counter).attr("onclick","removeAttr("+counter+")")
  $("#attribute"+counter).attr("readonly","true")
  counter += 1
  $("#addAttrTarget").append('<div><i id="addAttrButton'+counter+'" class="fa fa-plus-circle" onclick="handleAddAttributeClick()"></i><input type="text" id="attribute'+counter+'" name="attribute'+counter+'" placeholder="attribute: value" /></div>')
}
