$(document).ready(function() {

    $( "#ImageButton" ).click(function() {

        var user = 'joskvi';
        var currentUrl = window.location.hostname;
        var imageSource = 'http://localhost:5000/plot_img?user=' + user;

        var img = $( '<img id="ImagePlot" />' ).attr('src', imageSource).on('load', function() {

            if (!this.complete || typeof this.naturalWidth == "undefined" || this.naturalWidth == 0) {
                alert('The image is broken.');
            } else {

                if ($("#ImagePlot").length) {
                    $("#ImagePlot").replaceWith(img);
                } else {
                    $("#ImagePlotContainer").append(img);
                    $("#ImagePlotContainer").fadeIn();
                }
            }

        });
    });
});
