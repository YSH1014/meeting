function visit_url_and_refresh_current_page(href){
    $.ajax({
        type: 'GET',
        url: href,
        success: function (data) {
            window.location.reload();
        }
    });
}