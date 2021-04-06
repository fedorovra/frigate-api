from django.urls import path
from . import views


urlpatterns = [
    path('getmode/', views.api_getmode, name='getmode'),
    path('setmode/', views.api_setmode, name='setmode'),
    path('reboot/', views.api_reboot, name='reboot'),
    path('sms/send/', views.api_sms_send, name='sms-send'),
    path('ussd/', views.api_ussd, name='ussd'),
    path('signal/', views.api_signal, name='signal'),
    path('geo/', views.api_geo, name='geo'),
    path('sms/read/', views.api_sms_read, name='sms-read'),
    path('sms/delete/', views.api_sms_delete, name='sms-delete'),
    path('provider/', views.api_provider, name='provider'),
    path('check/', views.api_check, name='check'),
    path('keys/get/', views.api_keys_get, name='keys-get'),
    path('keys/create/', views.api_keys_create, name='keys-create'),
    path('keys/update/', views.api_keys_update, name='keys-update'),
    path('keys/delete/', views.api_keys_delete, name='keys-delete'),
    path('idle/', views.api_idle, name='idle'),
    path('modem/get/', views.api_modem_get, name='modem-get'),
    path('modem/create/', views.api_modem_create, name='modem-create'),
    path('modem/update/', views.api_modem_update, name='modem-update'),
    path('modem/delete/', views.api_modem_delete, name='modem-delete'),
    path('balance/', views.api_balance, name='balance'),
    path('switch/', views.api_switch, name='switch'),
]
