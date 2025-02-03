from sqlalchemy import (create_engine, Column, 
                        Integer, String, Date)
from sqlalchemy.orm import sessionmaker, declarative_base


engine = create_engine('sqlite:///inventory.db', echo=False)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    product_name = Column(String)
    product_price = Column(Integer)
    product_quantity = Column(Integer)
    date_updated = Column(Date)

    def __repr__(self):
        return f'{self.product_name} | {self.product_quantity} | {self.product_price} | {self.date_updated}'