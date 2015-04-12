function paginate_content(container_div_id) {

    var navigation_id = container_div_id + "_navigation"
    container_div = $("#" + container_div_id);

    container_div.before("<ul class='pagination' id='"+navigation_id +"'></ul>");

    navigation = $("#" + navigation_id);

    var number_of_items = container_div.children().size();

    var navigation_html = ''
    container_div.children().each(function(){
        var li_id = navigation_id + '_' + $(this).attr('id')
        navigation_html += '<li id="'+ li_id +'" ><a href=javascript:go_to_page("'+ li_id+ '","' + $(this).attr("id") + '")>'+ $(this).attr("title") +'</a></li>';
    });

    navigation.html(navigation_html);

    navigation.children().removeClass("disabled active");
    navigation.children().first().addClass("active");

    container_div.children().css('display', 'none');
    container_div.children().first().css('display', 'block');

}

function go_to_page(clicked_id, id) {

    requested_div = $("#" + id);
    container_div.children().css('display', 'none');
    $("#" + id).css('display', 'block');
    navigation.children().removeClass("disabled active");
    $("#" + clicked_id).addClass('active');
}