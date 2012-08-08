from django.contrib.auth import logout as auth_logout

def logout(request):
    auth_logout(request)
    return HttpResponseRedirect('/')

