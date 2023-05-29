from django.urls import path

from . import views


urlpatterns = [
    path('<int:user>', views.index, name="index"),
    path('enter_chat/', views.enter_chat, name='enter_chat')
]