import db
import sys
import requests
import json
from datetime import datetime



def query(resource):
    headers = {
               'AuthenticationToken': 'c9e52cb6-95b4-4ae3-b4bb-4cde692f3a4e',
               'Content-type': 'application/json',
               }

               data = '{"targetQuantity" : "2"}'

     r = requests.put('http://10.105.11.20:8080/webapp/api/v1/' + resource, headers=headers, data=data)

    )
    return r
    
costumer_id = 1
production_number = 1004

d = query('productionOrder/id/'.format(production_number)).json()

session = db.Session()

costumer = session.query(db.Costumer).get(costumer_id)





