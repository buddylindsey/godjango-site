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
});
