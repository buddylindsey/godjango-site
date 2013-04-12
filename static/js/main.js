$(document).ready(function() {
    switch (window.location.pathname) {
        // Used for Main Navigation
        case "/":
            $(".nav-home").addClass("active");
            break;
        case "/about/":
            $(".nav-about").addClass("active");
            break;
        case "/feedback/":
            $(".nav-feedback").addClass("active");
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

    $('.watch-video').click(function(){
        $('.video-preview').toggle();
        $('.video').toggle();
    });

    $(".video-favorite").click(function(){
        console.log($(".video-favorite").data('video'));
        $.ajax({
            type: "POST",
            url: "/favorite/add/",
            data: { video_pk: $(".video-favorite").data('video'), user_pk: $(".video-favorite").data('user') },
            dataType: "json",
            success: function() {
                $(".video-favorite").html("Favorited");
            }
        });
    });

    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    var csrftoken = getCookie('csrftoken');

});
