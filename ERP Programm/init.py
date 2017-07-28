import db

costumer = db.Costumer()

costumer.companyname = 'Nils AG'
costumer.streetname = 'Nilsstraße'
costumer.streetnumber = '16'
costumer.city = 'Darmstadt'
costumer.postalcode = '64409'
costumer.email = 'nils@ag.de'

session = db.Session()
session.add(costumer)
session.commit()
