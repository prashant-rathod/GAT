handleWindowResizeClick = function (targetWindow, el) {
    document.getElementById(targetWindow).style.display = document.getElementById(targetWindow).style.display == 'none' ? 'inline-block' : 'none'
    $(el).toggleClass('fa-window-restore')
}
$('[data-toggle="tooltip"]').tooltip();

// Placeholder message during resilience calculation
handleResilienceClick = function () {
    $("#resilience").attr("value", "Calculating Resilience...")
        .attr("data-original-title", "Resilience is being calculated. This is a heavy process and may require 1-2 minutes for completion.")
}

maximizeNLPTile = function (targetTileId, el) {
    var tiles = $("#tile-container").children();
    var targetTileObj = $("#" + targetTileId);
    var element = $(el);

    if (element.attr("class").includes("fa-window-maximize")) {
        tiles.each(function (index, target) {
            if (target.id == targetTileId) {
                setTilePosition(target, 0, 0);
                $(target).css("width", "100%");
            } else {
                $(target).hide();
            }
        });
        showFullNLPView();
    } else {
        showShortNLPView();
        restoreTiles();
    }
    element.toggleClass("fa-window-maximize fa-window-restore");
}
showFullNLPView = function () {
    $("#short-nlp").hide();
    $("#full-nlp").show();
}
showShortNLPView = function () {
    $("#short-nlp").show();
    $("#full-nlp").hide();
}
maximizeTile = function (targetTileId, el) {
    var tiles = $("#tile-container").children();
    var targetTileObj = $("#" + targetTileId);
    var element = $(el);

    if (element.attr("class").includes("fa-window-maximize")) {
        tiles.each(function (index, target) {
            if (target.id == targetTileId) {
                setTilePosition(target, 0, 0);
                $(target).css("width", "100%");
            } else {
                $(target).hide();
            }
        });
    } else {
        restoreTiles();
    }
    element.toggleClass("fa-window-maximize fa-window-restore");
}
closeVisualizationWindow = function (id, el) {
    $('#' + id).hide();
}