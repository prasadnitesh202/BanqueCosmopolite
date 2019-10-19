from django.urls import path
from . import views


app_name = 'main'  # here for namespacing of urls.

urlpatterns = [
    path("", views.home, name="home"),
    path('chatbot/', views.chatbot, name='chatbot'),
    path('login/', views.login, name='login'),
    path('account/', views.account, name='account'),
    

]