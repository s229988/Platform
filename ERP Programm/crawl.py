import db
import sys
import requests
import json
from datetime import datetime



def query(resource):
    r = requests.get('http://10.105.11.20:8080/webapp/api/v1/' + resource,
        headers={'AuthenticationToken': 'c9e52cb6-95b4-4ae3-b4bb-4cde692f3a4e'}
    )
    return r
    
costumer_id = 1
production_number = 1004

d = query('productionOrder/?productionOrderNumber-eq={}'.format(production_number)).json()

session = db.Session()

costumer = session.query(db.Costumer).get(costumer_id)

if 'result' in d and len(d['result']) > 0:
    r = d['result'][0]
    order = db.Order()
    try:
        order.article_id = r['articleId']
        order.amount = r['targetQuantity']
        order.create_date = datetime.fromtimestamp(r['createdDate'] / 1000)
        order.start_date = datetime.fromtimestamp(r['targetStartDate'] / 1000)
        order.end_date = datetime.fromtimestamp(r['targetEndDate'] / 1000)
    except NameError as e:
        sys.exit('Error {}'.format(e.what()))
    
    article_number = r['articleNumber']     
    d = query('article/?articleNumber-eq={}'.format(article_number)).json()
       
    if 'result' in d and len(d['result']) > 0:
        r = d['result'][0]
        article_image_id = r['articleImages'][0]['id']
        order.price_offer = r['articlePrices'][0]['price']
        
        r = query('article/id/{}/downloadArticleImage?articleImageId={}'.format(order.article_id, article_image_id))
        
        order.article_image = r.content
    else:
        print('No result for article with number', article_number)

    costumer.orders.append(order)
    
    session.add(costumer)
    session.commit()
else:
    print('No result for production order with article number', article_number)
