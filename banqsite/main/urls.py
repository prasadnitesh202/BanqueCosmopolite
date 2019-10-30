from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static



app_name = 'main'  # here for namespacing of urls.

urlpatterns = [
    path("", views.home, name="home"),
    path('chatbot/', views.chatbot, name='chatbot'),
    path('login/', views.login_req, name='login'),
    path('account/', views.account, name='account'),
    path('logout/', views.logout_request, name='logout'),
    path('webhook/', views.webhook, name='webhook'),
    path('ajax/', views.chatbot_ajax, name='chatbot_ajax'),
    path('atm_finder/', views.atmf, name='atm_finder'),
    path('checking/', views.checkin, name='checking'),
    path('cash_mgmt/', views.cash_mgmt, name='cash_mgmt'),
    path('monket/', views.monket, name='monket'),
    path('hsave/', views.hsave, name='hsave'),
    path('prepaid/', views.prepaid, name='prepaid'),
    path('savings/', views.savings, name='savings'),
    path('transaction/', views.transaction, name='transaction'),
    path('cards/', views.cards, name='cards'),
    path('payment/', views.payment, name='payment'),
    path('mission/', views.mission, name='mission'),
    path('team/', views.team, name='team'),
    path('history/', views.history, name='history'),
    ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)