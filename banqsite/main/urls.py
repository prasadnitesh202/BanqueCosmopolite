from django.urls import path
from . import views


app_name = 'main'  # here for namespacing of urls.

urlpatterns = [
    path("", views.home, name="home"),
    path('chatbot/', views.chatbot, name='chatbot'),
    path('login/', views.login_req, name='login'),
    path('account/', views.account, name='account'),
    path('logout/', views.logout_request, name='logout'),
    path('webhook/', views.webhook, name='webhook'),
    path('ajax/', views.ajax, name='ajax'),
    path('atm_finder/', views.atmf, name='atm_finder'),
    path('checking/', views.checkin,name='checking'),
    path('cash_mgmt/', views.cash_mgmt,name='cash_mgmt'),
    path('monket/', views.monket,name='monket'),
    path('hsave/', views.hsave,name='hsave'),
    path('prepaid/', views.prepaid,name='prepaid'),
    path('savings/', views.savings,name='savings'),
    

]