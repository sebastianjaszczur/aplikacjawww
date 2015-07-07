
var editors = $('textarea[data-ckeditor-config]');

function load_script(url, callback) {
    var script = document.createElement("script");
    script.type = "text/javascript";
    script.onload = callback;
    script.src = url;
    document.body.appendChild(script);
}

if(editors.length !== 0) {
    load_script(ckeditor_js_path, function() {
        editors.each(function(){
            var config = $(this).data('ckeditor-config');
            config.height = Math.max($(window).height() - 460, 300);

	        CKEDITOR.replace(this, config);

        });
    });

    load_script(ckeditor_highlight_js_path, function() {
        hljs.initHighlightingOnLoad();
    });
}



function handle_registration_change(workshop_name_txt, register) {
    var proper_url;
    if(register) {
        proper_url = register_to_workshops_url;
    } else {
        proper_url = unregister_to_workshops_url;
    }

    function error(message) {
        var elem = $('<div class="alert alert-danger fade in"><a href="#" class="close" data-dismiss="alert">&times;</a>' +
                     '<strong>Error!</strong> <span></span></div>');
        elem.find('span').text(message);
        $("#" + workshop_name_txt).after(elem); // add the error to the dom
    }

    $.ajax({
        url : proper_url, // the endpoint
        type : "POST", // http method
        data : { workshop_name : workshop_name_txt }, // data sent with the post request

        // handle a successful response
        success : function(json) {
            if (json.error) {
                error(json.error);
            } else if (json.redirect) {
                window.location.href = json.redirect;
            } else {
                $("#" + workshop_name_txt).find(".button-div").replaceWith(json.content);
            }
        },
        error: function(xhr, errmsg, errcode) {
            error('Wystąpił problem przy wysyłaniu danych (' + xhr.status + ': ' + errcode + ').');
        }
    });
}
