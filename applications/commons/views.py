from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

def login_view(request):
    if request.user.is_authenticated:
        return redirect('protected_view')
    
    return render(request, 'auth/login.html')


@login_required
def protected_view(request):
    user = request.user
    context = {
        'user': user,
        'is_google_user': hasattr(user, 'socialaccount_set') and user.socialaccount_set.filter(provider='google').exists()
    }
    return render(request, 'auth/protected.html', context)


def logout_view(request):

    logout(request)
    return redirect('login_view')