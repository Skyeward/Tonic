import pymysql as sql
from models.customer import Customer
from models.drink import Drink
from models.drink_order import DrinkOrder


def sql_connect_wrapper(func, *args):
    connection = sql.connect(host = "localhost", port = 33066, user = "root", passwd = "password", db = "TonicDB", autocommit = True)
    cursor = connection.cursor()
    
    func_return = func(cursor, *args)
    
    cursor.close()
    connection.close()

    return func_return


def test(cursor):
    cursor.execute('SELECT drinkID, drinkAvailable FROM Drinks WHERE drinkName = "tea"')
    #cursor.execute('SELECT drinkID FROM Drinks WHERE drinkName = "sea"')
    rows = cursor.fetchall()

    print(rows)


def add_drink(cursor, drink):
    cursor.execute(f'SELECT drinkAvailable FROM Drinks WHERE drinkName = "{drink}"')
    result = cursor.fetchall()

    if len(result) == 0:
        drink_exists = False
    else:
        drink_exists = True

    print(drink_exists)


def get_all_drinks(cursor):
    cursor.execute("SELECT drinkName FROM Drinks WHERE drinkAvailable = 1")
    results = cursor.fetchall()
    
    drink_list = []

    for result in results:
        new_drink = Drink()
        new_drink.name = result[0]
        drink_list.append(new_drink)

    return drink_list


def get_all_customers(cursor):
    cursor.execute("SELECT customerName, favouriteDrink FROM Customers WHERE active = 1")
    results = cursor.fetchall()
    
    customer_list = []

    for result in results:
        new_customer = Customer()
        new_customer.name = result[0]
        favourite = results[1]

        new_customer.favourite_drink = favourite
        customer_list.append(new_customer)

    return customer_list