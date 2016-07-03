$(document).ready(function() {

    // Processes the user input on the form
    $('#inputUsername').on('submit', function(e) {

        e.preventDefault()

        // Key-valued pairs of the form_data
        var form_data = $('form').serializeArray().reduce(function(obj, item) {
            obj[item.name] = item.value;
            return obj;
        }, {});

        var username = form_data['username'];

        // Send get request with the form data
        var request = $.ajax({

            url: 'http://localhost:5000/load_user_data',
            type: 'GET',
            data: $('form').serialize(),
            statusCode: {

                // Reponse from server is ok, and image will be printed
                200: function (response) {
                    writeResponse(response);
                    loadImage(username);
                },

                // The input data is invalid
                202: function (response) {
                    writeResponse(response);
                }
            }

        });

    });

});

// Write the server response to the DOM
function writeResponse(response) {

    var output = '<p id="submitResponse">' + response + '</p>';
    if ($("#submitResponse").length) {
        $("#submitResponse").replaceWith(output);
    } else {
        $("#ImagePlotContainer").append(output);
        $("#ImagePlotContainer").fadeIn();
    }

}

// Load the plot image from the server and write the image to the DOM
function loadImage(username) {

    var imageSource = 'http://localhost:5000/plot_img?username=' + username;

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
}
