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

NewsletterView = Backbone.View.extend
  el: $("form.newsletter")
  events:
    "submit": "addsubscriber"
  addsubscriber: (e) ->
    e.preventDefault()
    email = new Email()
    email_data =
      first_name: @$el.find('input[name=first_name]').val()
      last_name: @$el.find('input[name=last_name]').val()
      email: @$el.find('input[name=email]').val()
    email.save email_data,
      success: (email) ->
        console.log email
        return
    return

new NewsletterView()


#sublime.ready ->
  #player = sublime('video-player')

  #player.on 'end', () ->
    #$('#newsletter-modal').modal('show')
    #return
