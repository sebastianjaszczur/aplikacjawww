
$('textarea[data-ckeditor-config]').each(function(){
    var config = $(this).data('ckeditor-config');
    config.height = Math.max($(window).height() - 460, 300);
	CKEDITOR.replace(this, config);
});
