from models import (Base, session, 
                    Product, engine)
import csv
import datetime
import time


def menu():
    while True:
        print('''\nPROGRAMMING BOOKS
              \r1) Add books
              \r2) View all books
              \r3) Search for book
              \r4) Book Analysis
              \r5) Exit ''')
        choice = input('What would you like to do? ')
        if choice in ['1', '2','3','4','5']:
            return choice
        else:
            input('''
                  Please choose one of the options above.
                  A number from 1 to 5
                  Please try again. ''')


def clean_date(date_str):
    split_date = date_str.split('/')
    try:
        year = int(split_date[2])
        month = int(split_date[0])
        day = int(split_date[1])
        return_date =  datetime.date(year, month, day)
    except (ValueError, IndexError):
        input('''
                \n****** DATE ERROR ******
                \r The date format should include a valid date month/day/year
                \rEX: 02/20/1984
                \rPress enter to try again
                \r**************************''')
        return
    else:
        return return_date
   
def clean_price(price_str):
    try:
        slice_price = price_str[1:]
        float_price = float(slice_price)
    except ValueError:
        input('''
                \n****** PRICE ERROR ******
                \r The price should be a number without a currency symbol
                \rEX: 23.8
                \rPress enter to try again
                \r**************************''')
    else:
        return int(float_price * 100)
    
    
    
    

def add_csv():
    with open('inventory.csv') as csvfile:
        data = csv.reader(csvfile)
        for row in data:
            product_in_db = session.query(Product).filter(Product.product_name==row[0]).one_or_none()
            if product_in_db == None:
                product_name = row[0]
                product_price = clean_price(row[1])
                product_quantity = row[2]
                date_updated = clean_date(row[3])
                new_product = Product(product_name=product_name, product_price=product_price, product_quantity=product_quantity, date_updated= date_updated)
                session.add(new_product)
        session.commit()

        
            











def app():
    app_running = True
    while app_running:
        choice = menu()
        if   choice == '1':
            product_name = input('Product name: ')
            price_error = True
            while price_error:
                product_price = input('Product price: ')
                product_price = clean_price(product_price)
                if type(product_price) == int:
                    price_error = False
            product_quantity = input('Product quantity: ')
            date_error = True
            while date_error:
                date_updated = input('date updated(Ex: 11/1/2018): ')
                date_updated = clean_date(date_updated)
                if type(date_updated) == datetime.date:
                    date_error = False
            new_product = Product(product_name = product_name, product_price= product_price, product_quantity=product_quantity, date_updated = date_updated)
            session.add(new_product)
            session.commit()
            print('Product added to the inventory! ')
            time.sleep(1.5)
        elif choice == '2':
            for product in session.query(Product):
                print(f'{product.id} | {product.product_name} | {product.product_price} | {product.product_quantity} | {product.date_updated}')
            input('\nPress enter to return to the main menu')
        elif choice == '3':
            pass
        elif choice == '4':
            pass
        else:
            print('GOODBYE!')
            app_running = False




if __name__ == "__main__":
    Base.metadata.create_all(engine)
    add_csv()
    app()

    # for product in session.query(Product):
    #     print(product)
   