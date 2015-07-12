
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

$('.points-input').each(function() {
    var elem = $(this);
    var workshop_participant_id = elem.data('id');
    var save_btn = elem.parent().find('.save');
    var saved_value = elem.val();
    var qualified_mark = elem.parent().parent().find('.qualified-mark');

    save_btn.addClass('invisibile').click(function() {
        $.ajax({
            'url': '/savePoints/',
            'data': {'points': elem.val(), 'id': workshop_participant_id},
            'error': function(xhr, textStatus, errorThrown) {
                alert('Błąd: ' + errorThrown);
            },
            'method': 'POST',
            'success': function(value) {
                if(value.error) {
                    alert('Błąd: ' + errorThrown);
                } else {
                    saved_value = value.value;
                    elem.val(saved_value);
                    save_btn.addClass('invisibile');
                    qualified_mark.html(value.mark);
                }
            }
        });
    });

    elem.on('change keyup mouseup', function() {
        if(elem.val() != saved_value)
            save_btn.removeClass('invisibile');
    });
});

// really bad copy-paste ;_;

$('.comment-input').each(function() {
    var elem = $(this);
    var workshop_participant_id = elem.data('id');
    var save_btn = elem.parent().find('.savec');
    var saved_value = elem.val();
    var qualified_mark = elem.parent().parent().find('.qualified-mark');

    save_btn.addClass('invisibile').click(function() {
        $.ajax({
            'url': '/savePoints/',
            'data': {'comment': elem.val(), 'id': workshop_participant_id},
            'error': function(xhr, textStatus, errorThrown) {
                alert('Błąd: ' + errorThrown);
            },
            'method': 'POST',
            'success': function(value) {
                if(value.error) {
                    alert('Błąd: ' + errorThrown);
                } else {
                    save_btn.addClass('invisibile');
                    qualified_mark.html(value.mark);
                }
            }
        });
    });

    elem.on('change keyup mouseup', function() {
        if(elem.val() != saved_value)
            save_btn.removeClass('invisibile');
    });
});

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
