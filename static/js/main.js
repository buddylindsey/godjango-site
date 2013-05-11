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

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    function sameOrigin(url) {
        // test that a given url is a same-origin URL
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
                // Send the token to same-origin, relative URLs only.
                // Send the token only if the method warrants CSRF protection
                // Using the CSRFToken value acquired earlier
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    $(".add-to-cart").click(function(){
        $.ajax({
            url: "/cart/add/",
            type: 'POST',
            data: {'video_pk': $(".add-to-cart").data("id")},
            dataType: "json",
            success: function(){
                console.log("All is done well");
            }
        });
    });

});
