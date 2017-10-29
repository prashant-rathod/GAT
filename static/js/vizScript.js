handleWindowResizeClick = function(targetWindow,el) {
  document.getElementById(targetWindow).style.display = document.getElementById(targetWindow).style.display == 'none' ? 'inline-block' : 'none'
  $(el).toggleClass('fa-window-minimize')
  $(el).toggleClass('fa-window-maximize')
}
$('[data-toggle="tooltip"]').tooltip();

// Placeholder message during resilience calculation
handleResilienceClick = function() {
    $("#resilience").attr("value","Calculating Resilience...")
                    .attr("data-original-title","Resilience is being calculated. This is a heavy process and may require 1-2 minutes for completion.")
}
