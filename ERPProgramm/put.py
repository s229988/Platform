import requests

def query(resource):
    headers = {'AuthenticationToken': 'c9e52cb6-95b4-4ae3-b4bb-4cde692f3a4e', 'Content-type': 'application/json',}
    # Wie komme ich die Ebene tiefer? So wie ich es hier gemacht hab ist es offensichtlich falsch!
    data = '{"name" : "Test"}'

    r = requests.put('http://10.105.11.20:8080/webapp/api/v1/' + resource, headers=headers, data=data)
    print(r)
    return r

article_id = 6569

d = query('article/id/{}'.format(article_id))