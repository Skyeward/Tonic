import pymysql as sql
from models.customer import Customer
from models.drink import Drink
from models.drink_order import DrinkOrder


def sql_connect_wrapper(func, *args):
    "Give a sql function to run and arguments to pass to that function. Connects and disconnects from the database either side of the function call."
    
    connection = sql.connect(host = "localhost", port = 33066, user = "root", passwd = "password", db = "TonicDB", autocommit = True)
    cursor = connection.cursor()
    
    func_return = func(cursor, *args)
    
    cursor.close()
    connection.close()

    return func_return
   

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


def get_all_drinks(cursor):
    cursor.execute("SELECT drinkName FROM Drinks WHERE drinkAvailable = 1")
    results = cursor.fetchall()
    
    drink_list = []

    for result in results:
        new_drink = Drink()
        new_drink.name = result[0]
        drink_list.append(new_drink)

    return drink_list


def add_drink(cursor, drink):
    cursor.execute(f'SELECT drinkAvailable FROM Drinks WHERE drinkName = "{drink.name}"')
    result = cursor.fetchall()

    print(result)

    if len(result) == 0:
        print("drink doesn't exist")
        drink_exists = False
    else:
        print("drink exists")
        drink_exists = True

    if drink_exists:
        cursor.execute(f"UPDATE Drinks SET drinkAvailable = 1 WHERE drinkName = '{drink.name}'")
    else:
        cursor.execute(f"INSERT INTO Drinks (drinkName, drinkAvailable) VALUES ('{drink.name}', 1)")


def remove_drink(cursor, drink):
    print(drink.name)
    cursor.execute(f"UPDATE Drinks SET drinkAvailable = 0 WHERE drinkName = '{drink.name}'")