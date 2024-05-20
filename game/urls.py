from django.urls import path
from .views import CreateGameView
from django.contrib.auth.views import LogoutView

app_name = 'game'

urlpatterns = [
    path('', CreateGameView.as_view(), name='create'),
]
