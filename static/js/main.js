$(document).ready(function() {
    switch (window.location.pathname) {
        // Used for Main Navigation
        case "/browse/":
            $(".nav-home").addClass("active");
            break;
        case "/about/":
            $(".nav-about").addClass("active");
            break;
        case "/feedback/":
            $(".nav-feedback").addClass("active");
            break;
        case "/blog/":
            $(".nav-blog").addClass("active");
            break;

            // Used for sub nav on accounts
        case "/accounts/dashboard/":
            $(".account-dashboard").addClass("active");
            break;
        case "/accounts/favorites/":
            $(".account-favorites").addClass("active");
            break;
        case "/accounts/settings/":
            $(".account-settings").addClass("active");
            break;
        case "/accounts/billing/":
            $(".account-billing").addClass("active");
            break;
    }

    $('#content-tabs a:first').tab('show');

    $('#video-comments').on('click', function(event){
        window._gaq.push(['_trackEvent', 'Video-Meta', 'comments', null, null, false])
    });

    $('#video-show-notes').on('click', function(event){
        window._gaq.push(['_trackEvent', 'Video-Meta', 'show-notes', null, null, false])
    });

    $('#video-description').on('click', function(event){
        window._gaq.push(['_trackEvent', 'Video-Meta', 'description', null, null, false])
    });

    $('.watch-video').click(function(){
        window._gaq.push(['_trackEvent', 'Video', 'watch-video', null, null, false])
        $('.video-preview').toggle();
        $('.video-standard').toggle();
        $('.video-wide').toggle();
    });

    $(".video-favorite").click(function(){
        var el = $(this);
        $.ajax({
            type: "POST",
            url: "/favorite/add/",
            data: {
              video_pk: el.data('video'),
              is_favorite: el.data('favorite')
            },
            dataType: "json",
            success: function(data) {
              if(data.status == 'removed'){
                el.attr('src', '/static/img/nofav.png');
                window._gaq.push(['_trackEvent', 'Video-Meta', 'favorite', 'unfavorite', null, false])
              } else {
                el.attr('src', '/static/img/favorite.png');
                window._gaq.push(['_trackEvent', 'Video-Meta', 'favorite', 'favorite', null, false])
              }
            }
        });
    });

    $(".add-to-cart").click(function(){
        $.ajax({
            url: "/cart/add/",
            type: 'POST',
            data: {'video_pk': $(".add-to-cart").data("id")},
            dataType: "json",
            success: function(){}
        });
    });

});
