$(document).ready(function() {

  if(window.location.pathname === "/about/"){
    $(".nav-about").addClass("active");
  }

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
});
