from models import (Base, session, 
                    Product, engine)
import csv
import datetime
import time


def menu():
    while True:
        print('''\nPROGRAMMING BOOKS
              \r a) A - add a new product 
              \r b) B : for back up work on it later
              \r v) V : view the details of a single 
              \r x) Exit ''')
        choice = input('What would you like to do? ')
        if choice in ['a', 'b','v', 'x']:
            return choice
        else:
            input('''
                  Please choose one of the options above.
                  a, b, v or x for exit
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
    
def clean_id(id_str,options):
    try:
        product_id = int(id_str)
    except ValueError:
        input('''
                \n****** ID ERROR ******
                \r The id should be a number.
                \rPress enter to try again
                \r**************************''')
        return
    else:
        if product_id in options:
            return product_id
        else:
             input(f'''
                \n****** ID ERROR ******
                \r Options: {options}
                \rPress enter to try again
                \r**************************''')
        return


    
    

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
        if   choice == 'a': # to add a product 
            product_name = input('Product name: ')
            price_error = True
            while price_error:
                product_price = input('Product price: ')
                product_price = clean_price(product_price)
                if type(product_price) == int:
                    price_error = False
            product_quantity = input('Product quantity: ')
            date_error = True
            # while date_error:
            #     date_updated = input('date updated(Ex: 11/1/2018): ')
            #     date_updated = clean_date(date_updated)
            #     if type(date_updated) == datetime.date:
            #         date_error = False
            new_product = Product(product_name = product_name, product_price= product_price, product_quantity=product_quantity)
            session.add(new_product)
            session.commit()
            print('Product added to the inventory! ')
            time.sleep(1.5)
        elif choice == 'b': # for the back up
            for product in session.query(Product):
                print(f'{product.id} | {product.product_name} | {product.product_price} | {product.product_quantity} | {product.date_updated}')
            input('\nPress enter to return to the main menu')
        elif choice == 'v': # to view a single product.
            id_options = []
            for product in session.query(Product):
                id_options.append(product.id)
            id_error = True
            while id_error:
                id_choice = input(f'''
                    \n Id Options: {id_options}
                    \nProduct id: ''')
                id_choice = clean_id(id_choice, id_options)
                if type(id_choice) == int:
                    id_error = False
            the_product = session.query(Product).filter(Product.id== id_choice).first()
            print(f'{the_product.product_name} | {the_product.product_quantity} | ${the_product.product_price /100} | {the_product.date_updated}')
            input('\nPrint enter to return to themain menu')
        else:
            print('GOODBYE!')
            app_running = False




if __name__ == "__main__":
    Base.metadata.create_all(engine)
    add_csv()
    app()

    # for product in session.query(Product):
    #     print(product)
   