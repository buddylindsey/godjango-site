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

app = angular.module('godjango', [])

app.config(['$httpProvider', ($httpProvider) ->
      $httpProvider.defaults.xsrfCookieName = 'csrftoken'
      $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken'
      return
])

app.controller('NewsletterForm', ['$scope', ($scope)->
    $scope.save = (user)->
      alert user.email

      $.ajax
        type: "POST"
        url: "/api/subscriber/create/"
        data:
          email: user.email
          first_name: user.first_name
          last_name: user.last_name
        dataType: "json"
        success: (data) ->
          $("#newsletter-message").html("Thank you for subscribing.")
          $("#newsletter-message").addClass("alert alert-success")
          $(".newsletter-email-message").removeClass("alert alert-danger")
          return
        error: (data) ->
          $(".newsletter-email-message").html(data.responseJSON.email[0])
          $(".newsletter-email-message").addClass("alert alert-danger")
          return
      return
    return
  ])
