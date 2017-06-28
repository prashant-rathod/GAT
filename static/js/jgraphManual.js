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
  for (var feature in currentNodeDict['attributes']) {
    if (feature != 'name') {
      $("#editAttributeInfo").append('<span>'+feature+': </span><input class="editInputs"id="'+feature+'" name="'+feature+'" value="'+currentNodeDict['attributes'][feature]+'"></input><br />');
    }
  }
  $("#editAttributeInfo").append('<input id="editSubmitButton" type="submit" name="editSubmitButton" value="Submit" onclick="handleEditSubmit(currentNodeDict)" />')
  $("#editAttributeInfo").append("<div class='centeredIcon' onclick='toggleEditWindow()'><i class='fa fa-arrow-circle-down'></i></div>")
};

toggleEditWindow = function() {
  $("#attributeInfo").toggleClass("closed")
  $("#editAttributeInfo").toggleClass("closed")
}

showAddNodeWindow = function() {
  $("#toolbar").toggleClass("closed")
  $("#addNodeWindow").toggleClass("closed")
}
