function send_points(field_name, elem, save_btn) {
    var workshop_participant_id = elem.data('id');
    var saved_value = elem.val();
    var qualified_mark = elem.parent().parent().find('.qualified-mark');

    save_btn.addClass('invisibile').click(function() {
        var data = {'id': workshop_participant_id};
        data[field_name] = elem.val();
        $.ajax({
            'url': '/savePoints/',
            'data': data,
            'error': function(xhr, textStatus, errorThrown) {
                alert('Błąd: ' + errorThrown);
            },
            'method': 'POST',
            'success': function(value) {
                if(value.error) {
                    alert('Błąd: ' + value.error);
                } else {
                    saved_value = value[field_name];
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
}

$('.points-input').each(function() {
    var elem = $(this);
    var save_btn = elem.parent().find('.save');
	send_points('points', elem, save_btn);
});

$('.comment-input').each(function() {
    var elem = $(this);
    var save_btn = elem.parent().find('.savec');
    send_points('comment', elem, save_btn);
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

$(function () {
    $('[data-toggle="popover"]').popover();

    // Automatically hide 'Saved successfully' alerts after 4 seconds
    $(".alert-info, .alert-success").delay(4000).fadeTo(500, 0).slideUp(500, function(){
        $(this).remove();
    });

    $('.dateinput').each(function (i, x) {
        var dates = [];
        for(var date = moment($(x).data('start-date')); date <= moment($(x).data('end-date')); date.add(1, 'days'))
            dates.push(date.toDate());
        $(x).datetimepicker({
            format: 'L',
            locale: 'pl',
            defaultDate: $(x).data('default-date'),
            enabledDates: dates,
        });
    });
});
