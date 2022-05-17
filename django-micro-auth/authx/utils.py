import requests
from django.conf import settings
from django.core.cache import cache

def fetch_service_data(id, url, use_cache = True):

        request_url = f'{url}{id}/'
        
        data = cache.get(request_url)
        if data and use_cache:
            return data
        
        r = requests.get(request_url, headers={'Authorization': f'Bearer {settings.SERVICE_API}'})
        r_status = r.status_code

        if r_status == 200:
            fetched_data = r.json()
            cache.set(request_url, fetched_data)
            return fetched_data

        return None