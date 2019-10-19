from django.urls import path
from . import views


app_name = 'main'  # here for namespacing of urls.

urlpatterns = [
    path("", views.home, name="home"),
    path('chatbot/', views.chatbot, name='chatbot'),
    path('login/', views.login_req, name='login'),
    path('account/', views.account, name='account'),
    path('logout/', views.logout_request, name='logout'),
    

]