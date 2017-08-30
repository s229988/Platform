from sqlalchemy import Column, ForeignKey, Integer, Float, String, DateTime, Binary
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Customer(Base):
    __tablename__ = 'customers'

    id = Column(Integer, primary_key=True)
    companyname = Column(String(100))
    streetname = Column(String(100))
    streetnumber = Column(String(100))
    city = Column(String(100))
    postalcode = Column(Integer)
    email = Column(String(100))
    orders = relationship('Order')

    def __repr__(self):
        return "<Customer(id={}, name={})>".format(self.id, self.name)

class Producer(Base):
    __tablename__ = 'producers'
    
    id = Column(Integer, primary_key=True)
    companyname = Column(String(100))
    streetname = Column(String(100))
    streetnumber = Column(String(100))
    city = Column(String(100))
    postalcode = Column(Integer)
    email = Column(String(100))
    number_machines = Column(Integer)
    machines = relationship('Machines')
    
    def __repr__(self):
        return "<Producer(id={}, name={})>".format(self.id, self.companyname)
    
class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('customers.id'), nullable=False)
    article_id = Column(Integer)
    article_image = Column(Binary)
    amount = Column(Integer)
    price_offer = Column(Float)
    create_date = Column(DateTime)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    status = Column(String(100))

    def __repr__(self):
        return "<Order(id={}. article_id={})>".format(self.id, self.article)
        
class Machines(Base):
    __tablename__ = 'machines'
    
    id = Column(Integer, primary_key=True)
    producer_id = Column(Integer, ForeignKey('producers.id'), nullable=False)
    capacity = Column(Integer)
    price = Column(Float)
    
    def __repr__(self):
        return "<Machines(id={}".format(self.id, self.capacity)
    
class Matches(Base):
    __tablename__ = 'matches'
    
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('orders.id'), nullable=False)
    machine_id = Column(Integer, ForeignKey('machines.id'), nullable=False)
    
    def __repr__(self):
        return "<Matches(id={}, status={})>".format(self.id, self.status)


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
engine = create_engine('mysql+mysqlconnector://root:iot17@127.0.0.1/website', echo=True)
Session = sessionmaker(bind=engine)

if __name__ == '__main__':
    Base.metadata.create_all(engine)
