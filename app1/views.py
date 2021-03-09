from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import JsonResponse
from time import sleep
import xmltodict
import requests
from requests_toolbelt.adapters import source
from django.http import Http404, HttpResponseForbidden
from django.core import serializers

from .models import APIKeys

tokens = ['F64e9CtMpmtjJLfJ','Q7cuaYgpBGj8xtphhbbAUEfZR',]


def api_keys_check(request, perm):
    try:
        key = APIKeys.objects.get(api_key=request.GET['key'])
    except Exception as error:
        return False
    else:
        if perm in key.permissions.split(',') and key.is_active == 'Y':
            return True
        else:
            return False


def get_modem_ip(modem):
    return '192.168.' + str(modem) + '.1'


def get_token(modem):
    try:
        resp = requests.get('http://' + get_modem_ip(modem) + '/api/webserver/SesTokInfo', timeout=1)
        token = xmltodict.parse(resp.text)['response']['TokInfo']
        session = xmltodict.parse(resp.text)['response']['SesInfo']
    except Exception as error:
        raise Http404()
    else:
        headers = { 'Cookie' : session, '__RequestVerificationToken' : token}
        return headers


def get_mode(modem):
    headers = get_token(modem)
    try:
        status = requests.get('http://' + get_modem_ip(modem) + '/api/net/net-mode', headers=headers)
    except Exception as error:
        raise Http404()
    else:
        return status.text


def api_keys_get(request):
    if request.method == 'GET':
        if api_keys_check(request, 'sys'):
            return JsonResponse(serializers.serialize('json', APIKeys.objects.all()), safe=False)
        else:
            return HttpResponseForbidden()


def api_keys_create(request):
    if request.method == 'GET':
        if api_keys_check(request, 'sys'):
            try:
                key = APIKeys.objects.create(api_key=request.GET['k'], permissions=request.GET['p'], is_active=request.GET['a'])
                key.save()
            except Exception as error:
                return JsonResponse({ 'status' : 'error' })
            else:
                return JsonResponse({ 'status' : 'ok'})
        else:
            return HttpResponseForbidden()


def api_keys_update(request):
    if request.method == 'GET':
        if api_keys_check(request, 'sys'):
            try:
                key = APIKeys.objects.get(id__exact=int(request.GET['pk']))
            except Exception as error:
                return JsonResponse({ 'status' : 'error' })
            else:
                if request.GET.get('p'):
                    key.permissions = request.GET['p']
                if request.GET.get('a'):
                    key.is_active = request.GET['a']
                key.save()
                return JsonResponse({ 'status' : 'ok'})
        else:
            return HttpResponseForbidden()


def api_keys_delete(request):
    if request.method == 'GET':
        if api_keys_check(request, 'sys'):
            try:
                key = APIKeys.objects.get(id__exact=int(request.GET['pk']))
                key.delete()
            except Exception as error:
                return JsonResponse({ 'status' : 'error' })
            else:
                return JsonResponse({ 'status' : 'ok'})
        else:
            return HttpResponseForbidden()


def api_getmode(request):
    if request.method == 'GET':
        if api_keys_check(request, 'mode'):
            return JsonResponse(xmltodict.parse(get_mode(request.GET['modem'])), safe=False)
        else:
            return HttpResponseForbidden()


def api_setmode(request):
    if request.method == 'GET':
        if api_keys_check(request, 'mode'):
            mode = xmltodict.parse(get_mode(request.GET['modem']))['response']['NetworkMode']
            if mode != '03':
                mode = '03'
            else:
                mode = '00'
            headers = get_token(request.GET['modem'])
            data = """
                   <?xml version=\"1.0\" encoding=\"UTF-8\"?>
                   <request>
                       <NetworkMode>""" + mode + """</NetworkMode>
                       <NetworkBand>3FFFFFFF</NetworkBand>
                       <LTEBand>7FFFFFFFFFFFFFFF</LTEBand>
                   </request>
                   """
            try:
                status = requests.post('http://' + get_modem_ip(request.GET['modem']) + '/api/net/net-mode', headers=headers, data=data)
            except Exception as error:
                raise Http404()
            else:
                return JsonResponse(xmltodict.parse(status.text), safe=False)
        else:
            return HttpResponseForbidden()


def api_reboot(request):
    if request.method == 'GET':
        if api_keys_check(request, 'reboot'):
            headers = get_token(request.GET['modem'])
            data = """
                   <?xml version=\"1.0\" encoding=\"UTF-8\"?>
                   <request>
                       <Control>1</Control>
                   </request>
                   """
            try:
                status = requests.post('http://' + get_modem_ip(request.GET['modem']) + '/api/device/control', headers=headers, data=data)
            except Exception as error:
                raise Http404()
            else:
                return JsonResponse(xmltodict.parse(status.text), safe=False)
        else:
            return HttpResponseForbidden()


def api_sms_send(request):
    if request.method == 'GET':
        if api_keys_check(request, 'sms'):
            headers = get_token(request.GET['modem'])
            data = """
                   <?xml version=\"1.0\" encoding=\"UTF-8\"?>
                   <request>
                       <Index>-1</Index>
                       <Phones>
                           <Phone>""" + request.GET['phone'] + """</Phone>
                       </Phones>
                       <Sca></Sca>
                       <Content>""" + request.GET['text'] + """</Content>
                       <Length>-1</Length>
                       <Reserved>-1</Reserved>
                       <Date>-1</Date>
                   </request>
                   """
            try:
                status = requests.post('http://' + get_modem_ip(request.GET['modem']) + '/api/sms/send-sms', headers=headers, data=data.encode('utf-8'))
            except Exception as error:
                raise Http404()
            else:
                return JsonResponse(xmltodict.parse(status.text), safe=False)
        else:
            return HttpResponseForbidden()


def api_sms_read(request):
    if request.method == 'GET':
        if api_keys_check(request, 'sms'):
            headers = get_token(request.GET['modem'])
            data = """
                   <?xml version=\"1.0\" encoding=\"UTF-8\"?>
                   <request>
                       <PageIndex>1</PageIndex>
                       <ReadCount>50</ReadCount>
                       <BoxType>1</BoxType>
                       <SortType>0</SortType>
                       <Ascending>0</Ascending>
                       <UnreadPreferred>0</UnreadPreferred>
                   </request>
                   """
            try:
                status = requests.post('http://' + get_modem_ip(request.GET['modem']) + '/api/sms/sms-list', headers=headers, data=data)
            except Exception as error:
                raise Http404()
            else:
                return JsonResponse(xmltodict.parse(status.text.encode('iso_8859_1')), safe=False, json_dumps_params={'ensure_ascii': False})
        else:
            return HttpResponseForbidden()


def api_sms_delete(request):
    if request.method == 'GET':
        if api_keys_check(request, 'sms'):
            headers = get_token(request.GET['modem'])
            data = """
                   <?xml version=\"1.0\" encoding=\"UTF-8\"?>
                   <request>
                       <Index>""" + request.GET['index'] + """</Index>
                   </request>
                   """
            try:
                status = requests.post('http://' + get_modem_ip(request.GET['modem']) + '/api/sms/delete-sms', headers=headers, data=data)
            except Exception as error:
                raise Http404()
            else:
                return JsonResponse(xmltodict.parse(status.text), safe=False)
        else:
            return HttpResponseForbidden()


def api_ussd(request):
    if request.method == 'GET':
        if api_keys_check(request, 'ussd'):
            headers = get_token(request.GET['modem'])
            data = """
                   <?xml version=\"1.0\" encoding=\"UTF-8\"?>
                   <request>
                      <content>*""" + request.GET['phone'] + """#</content>
                      <timeout>5</timeout>
                   </request>
                   """
            try:
                status = requests.post('http://' + get_modem_ip(request.GET['modem']) + '/api/ussd/send', headers=headers, data=data)
            except Exception as error:
                raise Http404()

            sleep(5)
            
            headers = get_token(request.GET['modem'])
            try:
                status = requests.get('http://' + get_modem_ip(request.GET['modem']) + '/api/ussd/get', headers=headers)
            except Exception as error:
                raise Http404()
            else:
                return JsonResponse(xmltodict.parse(status.text), safe=False)
        else:
            return HttpResponseForbidden()


def api_signal(request):
    if request.method == 'GET':
        if api_keys_check(request, 'net'):
            headers = get_token(request.GET['modem'])
            try:
                status = requests.get('http://' + get_modem_ip(request.GET['modem']) + '/api/device/signal', headers=headers)
            except Exception as error:
                raise Http404()
            else:
                return JsonResponse(xmltodict.parse(status.text), safe=False)
        else:
            return HttpResponseForbidden()


def api_provider(request):
    if request.method == 'GET':
        if api_keys_check(request, 'net'):
            headers = get_token(request.GET['modem'])
            try:
                status = requests.get('http://' + get_modem_ip(request.GET['modem']) + '/api/net/current-plmn', headers=headers)
            except Exception as error:
                raise Http404()
            else:
                return JsonResponse(xmltodict.parse(status.text), safe=False)
        else:
            return HttpResponseForbidden()


def api_geo(request):
    if request.method == 'GET':
        if api_keys_check(request, 'net'):
            headers = get_token(request.GET['modem'])

            try:
                status = requests.get('http://' + get_modem_ip(request.GET['modem']) + '/api/device/signal', headers=headers)
            except Exception as error:
                raise Http404()
            cid = xmltodict.parse(status.text)['response']['cell_id']

            status = requests.get('http://' + get_modem_ip(request.GET['modem']) + '/api/net/current-plmn', headers=headers)
            mcc = xmltodict.parse(status.text)['response']['Numeric'][0:3]
            mnc = xmltodict.parse(status.text)['response']['Numeric'][3:]

            data = "{\"token\": \"pk.f951ab6b8273e1e0a9d47fbea682052f\",\"radio\": \"lte\",\"mcc\": \"" + mcc + "\",\"mnc\": \"" + mnc + "\",\"cells\": [{\"lac\": 1,\"cid\": \"" + cid + "\",\"psc\": 0}],\"address\": 2}"
            try:
                status = requests.post('https://us1.unwiredlabs.com/v2/process.php', data=data)
            except Exception as error:
                raise Http404()
            else:
                import json
                return JsonResponse(json.loads(status.text), safe=False)
        else:
            return HttpResponseForbidden()


def api_check(request):
    if request.method == 'GET':
        if api_keys_check(request, 'sys'):
            modem_ip = get_modem_ip(request.GET['modem']) + '00'
            session = requests.Session()
            try:
                iface = source.SourceAddressAdapter(modem_ip)
                session.mount('https://', iface)
                ip = session.get('https://ipinfo.io/ip')
                org = session.get('https://ipinfo.io/org?token=a1b8eb50c0764e')
                city = session.get('https://ipinfo.io/city?token=a1b8eb50c0764e')
            except Exception as error:
                raise Http404()

            response = { 'response' : { 'int' : modem_ip, 'ext' : ip.text.rstrip("\n"), 'org' : org.text.rstrip("\n"), 'city' : city.text.rstrip("\n"), } }
            return JsonResponse(response, safe=False)
        else:
            return HttpResponseForbidden()

