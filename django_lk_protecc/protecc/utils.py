from django.conf import settings
import requests
import json

def block_ip_address(ip_address):
    headers = {
        'X-Auth-Email': settings.CL_AUTH_EMAIL,
        'X-Auth-Key': settings.CL_AUTH_KEY,
        'Content-Type': 'application/json',
    }

    data = {
        'ip': ip_address,
        'comment': f'blocked ip for {settings.SITE_NAME}' 
    }

    response = requests.post(
        f'https://api.cloudflare.com/client/v4/accounts/{settings.CL_ACCOUNT_ID}/rules/lists/{settings.CL_LIST_ID}/items',
        headers=headers,
        data=f'[{json.dumps(data)}]'
    )
    return response

def remove_blocked_ip_address(ip_address):

    headers = {
        'X-Auth-Email': settings.CL_AUTH_EMAIL,
        'X-Auth-Key': settings.CL_AUTH_KEY,
        'Content-Type': 'application/json',
    }

    list_response = requests.get(f'https://api.cloudflare.com/client/v4/accounts/{settings.CL_ACCOUNT_ID}/rules/lists/{settings.CL_LIST_ID}/items', headers=headers)
    if list_response.json()['success'] == False:
        return list_response

    list_item_id = next(item for item in list_response.json()['result'] if item['ip'] == ip_address)['id']

    data = {"items":[{"id": list_item_id}]}

    response = requests.delete(f'https://api.cloudflare.com/client/v4/accounts/{settings.CL_ACCOUNT_ID}/rules/lists/{settings.CL_LIST_ID}/items', headers=headers, data=json.dumps(data))
    return response

def get_cloudflare_list_items():
    headers = {
        'X-Auth-Email': settings.CL_AUTH_EMAIL,
        'X-Auth-Key': settings.CL_AUTH_KEY,
        'Content-Type': 'application/json',
    }

    response = requests.get(f'https://api.cloudflare.com/client/v4/accounts/{settings.CL_ACCOUNT_ID}/rules/lists/{settings.CL_LIST_ID}/items', headers=headers)
    return response
