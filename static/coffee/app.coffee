FavoriteView = Backbone.View.extend
  el: $(".video-favorite")
  events:
    "click": "submit"

  submit: ->
    $.ajax
      type: "POST"
      url: "/favorite/add/"
      data:
        video_pk: $(".video-favorite").data 'video'
        is_favorite: $(".video-favorite").data 'favorite'
      dataType: "json"
      success: (data) ->
        if(data.status == 'removed')
          $(".video-favorite").attr 'src', '/static/img/nofav.png'
          return
        else
          $(".video-favorite").attr 'src', '/static/img/favorite.png'
          return
    return

new FavoriteView()

Email = Backbone.Model.extend
  urlRoot: '/newsletter/email/'
  defaults:
    first_name: ''
    last_name: ''
    email: ''
