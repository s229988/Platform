import requests
import time

def query(resource):
    r = requests.get('http://10.105.11.20:8080/webapp/api/v1/' + resource,
        headers={'AuthenticationToken': 'c9e52cb6-95b4-4ae3-b4bb-4cde692f3a4e'}
    )
    return r.json()

actual_date = int(round(time.time() * 1000))
d = query('productionOrder/?targetStartDate-gt={}'.format(actual_date))
production_numbers = []


for e in d['result']:
    production_numbers.append(e['productionOrderNumber'])
        
print(production_numbers)
