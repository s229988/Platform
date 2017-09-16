from sys import exit
import requests

headers = {'AuthenticationToken': 'c9e52cb6-95b4-4ae3-b4bb-4cde692f3a4e', 'Content-type': 'application/json'}
url_base = 'http://10.105.11.20:8080/webapp/api/v1/'

article_nr = 6518
new_price = 667.77

url = url_base + 'article/id/{}'.format(article_nr)


# Get the article
r = requests.get(url, headers=headers)
if not r.status_code == 200: 
    exit('Fail')
article = r.json()

# Update the first price, we could also add one
try:
    prices = article['articlePrices']
    if len(prices) == 0:
        exit('Article has no prices')
    prices[0]['price'] = new_price
except KeyError as e:
    exit(str(e))

# Now update the whole article using put
requests.put(url, headers=headers, json=article)