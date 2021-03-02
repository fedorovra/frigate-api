from django.urls import path
from .views import api_getmode, api_setmode, api_reboot, api_sms_send, api_ussd, api_signal, api_geo, api_sms_read, api_sms_delete, api_provider, api_check

urlpatterns = [
    path('getmode/', api_getmode, name='getmode'),
    path('setmode/', api_setmode, name='setmode'),
    path('reboot/', api_reboot, name='reboot'),
    path('sms/send/', api_sms_send, name='sms-send'),
    path('ussd/', api_ussd, name='ussd'),
    path('signal/', api_signal, name='signal'),
    path('geo/', api_geo, name='geo'),
    path('sms/read/', api_sms_read, name='sms-read'),
    path('sms/delete/', api_sms_delete, name='sms-delete'),
    path('provider/', api_provider, name='provider'),
    path('check/', api_check, name='check'),
]
