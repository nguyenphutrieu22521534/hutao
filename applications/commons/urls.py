from django.urls import path

from .views import (
    login_view,
    protected_view,
    logout_view,
)
urlpatterns = [
    path('auth/login/', login_view, name='login_view'),
    path('auth/protected/', protected_view, name='protected_view'),
    path('auth/logout/', logout_view, name='logout_view'),

]
