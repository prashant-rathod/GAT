//---------------------
/*
Jgraph UI Scripts for Hermes 2.0
Author: Ryan Steed, 21 Jun 2017
*/
//---------------------

attributesToggle = function() {
  document.getElementById('measureInfo').style.display='none';
  document.getElementById('attributeInfo').style.display='inline-block';
  document.getElementById('propInfo').style.display='none';
  tablinks = document.getElementsByClassName("tablinks");
  for (i = 0; i < tablinks.length; i++) {
    tablinks[i].className = tablinks[i].className.replace(" active", "");
  }
  event.currentTarget.className += " active";
}
measuresToggle = function() {
  document.getElementById('measureInfo').style.display='inline-block';
  document.getElementById('attributeInfo').style.display='none';
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
  document.getElementById('attributeInfo').style.display='none';
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
