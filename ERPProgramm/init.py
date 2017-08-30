import db

customer = db.Customer()

customer.companyname = 'Nils AG'
customer.streetname = 'Nilsstraße'
customer.streetnumber = '16'
customer.city = 'Darmstadt'
customer.postalcode = '64409'
customer.email = 'nils@ag.de'

session = db.Session()
session.add(customer)
session.commit()


