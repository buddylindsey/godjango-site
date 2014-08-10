switch window.location.pathname
  #Used for Main Navigation
  when "/browse/"
    $(".nav-home").addClass("active")
  when "/about/"
    $(".nav-about").addClass("active")
  when "/feedback/"
    $(".nav-feedback").addClass("active")
  when "/blog/"
    $(".nav-blog").addClass("active")
  #Used for sub nav on accounts
  when "/accounts/dashboard/"
      $(".account-dashboard").addClass("active")
  when "/accounts/favorites/"
      $(".account-favorites").addClass("active")
  when "/accounts/settings/"
      $(".account-settings").addClass("active")
  when "/accounts/billing/"
      $(".account-billing").addClass("active")

$('#content-tabs a:first').tab('show')

$('#video-comments').on 'click', (event) ->
  window._gaq.push ['_trackEvent', 'Video-Meta', 'comments', null, null, false]
  return

$('#video-show-notes').on 'click', (event) ->
  window._gaq.push ['_trackEvent', 'Video-Meta', 'show-notes', null, null, false]
  return

$('#video-description').on 'click', (event) ->
  window._gaq.push ['_trackEvent', 'Video-Meta', 'description', null, null, false]
  return

$('.watch-video').click ->
  window._gaq.push ['_trackEvent', 'Video', 'watch-video', null, null, false]
  $('.video-preview').toggle()
  $('.video-standard').toggle()
  $('.video-wide').toggle()
  return

$(".video-favorite").click ->
  el = $(this)
  $.ajax
    type: "POST"
    url: "/favorite/add/"
    data:
      video_pk: el.data('video')
      is_favorite: el.data('favorite')
    dataType: "json"
    success: (data) ->
      if(data.status == 'removed')
        el.attr('src', '/static/img/nofav.png')
        window._gaq.push(['_trackEvent', 'Video-Meta', 'favorite', 'unfavorite', null, false])
        return
      else
        el.attr('src', '/static/img/favorite.png')
        window._gaq.push(['_trackEvent', 'Video-Meta', 'favorite', 'favorite', null, false])
        return
  return

$("#newsletter-subscribe").on 'submit', (e) ->
  $("#newsletter-subscribe-button").prop "disabled", true
  e.preventDefault()
  $.ajax
    type: "POST"
    url: "/accounts/newsletter-subscribe/"
    data: $("#newsletter-subscribe").serializeArray()
    dataType: "json"
    success: (data) ->
      element = $('#newsletter-message')
      if data.success
        element.removeClass 'alert alert-error'
        element.addClass 'alert alert-success'
        element.html data.success
      if data.errors
        $('#newsletter-subscribe-button').prop "disabled", false
        element.removeClass 'alert alert-success'
        element.addClass 'alert alert-error'
        if data.errors.email
          element.append("Email: " + d) for d in data.errors.email
        if data.errors.general
          element.append(d) for d in data.errors.general
      return
  return

sublime.ready ->
  player = sublime('video-player')

  player.on 'end', () ->
    $('#newsletter-modal').modal('show')
    return
