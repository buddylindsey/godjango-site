$(document).ready(function() {
  switch (window.location.pathname) {
    case "/":
      $(".nav-home").addClass("active");
      break;
    case "/about/":
      $(".nav-about").addClass("active");
      break;
    case "/feedback/":
      $(".nav-feedback").addClass("active");
      break;
  }

  $('#content-tabs a:first').tab('show');

  $('.watch-video').click(function(){
    $('.video-preview').toggle();
    $('.video').toggle();
  });
});
