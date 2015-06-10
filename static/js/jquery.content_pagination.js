var container_div;

function paginate_content(container_div_id) {
    var navigation_id = container_div_id + "_navigation";

    container_div = $("#" + container_div_id);

    container_div.before("<ul class='pagination' id='"+navigation_id +"'></ul>");

    navigation = $("#" + navigation_id);

    var number_of_items = container_div.children().size();

    container_div.children().each(function(){
        var elem = $(this);
        var li_id = navigation_id + '_' + elem.attr('id');

        var child = $('<li>').attr('id', li_id).append(
            $('<a>').attr('href', '#' + elem.attr('id')).text(elem.attr("title")).click(function() {
                go_to_page(navigation_id, elem.attr('id'));
            })
        );
        navigation.append(child);
    });

    navigation.children().removeClass("disabled active");
    navigation.children().first().addClass("active");

    container_div.children().css('display', 'none');
    container_div.children().first().css('display', 'block');
}

function go_to_page(navigation_id, id) {
    var clicked_id = navigation_id + '_' + id;
    console.log(clicked_id);
    container_div.children().css('display', 'none');

    $("#" + id).css('display', 'block');
    navigation.children().removeClass("disabled active");
    $("#" + clicked_id).addClass('active');
}
