handleWindowResizeClick = function(targetWindow,el) {
  document.getElementById(targetWindow).style.display = document.getElementById(targetWindow).style.display == 'none' ? 'inline-block' : 'none'
  $(el).toggleClass('fa-window-minimize')
  $(el).toggleClass('fa-window-maximize')
}
$('[data-toggle="tooltip"]').tooltip();
