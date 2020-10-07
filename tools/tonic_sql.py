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
        favourite = result[1]

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

    if len(result) == 0:
        drink_exists = False
    else:
        drink_exists = True

    if drink_exists:
        cursor.execute(f"UPDATE Drinks SET drinkAvailable = 1 WHERE drinkName = '{drink.name}'")
    else:
        cursor.execute(f"INSERT INTO Drinks (drinkName, drinkAvailable) VALUES ('{drink.name}', 1)")


def remove_drink(cursor, drink):
    cursor.execute(f"UPDATE Drinks SET drinkAvailable = 0 WHERE drinkName = '{drink.name}'")


def add_customer(cursor, customer):
    cursor.execute(f'SELECT active FROM Customers WHERE customerName = "{customer.name}"')
    result = cursor.fetchall()

    if len(result) == 0:
        #print("drink doesn't exist")
        customer_exists = False
    else:
        #print("drink exists")
        customer_exists = True

    if customer_exists:
        cursor.execute(f"UPDATE Customers SET favouriteDrink = '{customer.favourite_drink}', active = 1 WHERE customerName = '{customer.name}'")
    else:
        cursor.execute(f"INSERT INTO Customers (customerName, favouriteDrink, active) VALUES ('{customer.name}', '{customer.favourite_drink}', 1)")


def remove_customer(cursor, customer):
    cursor.execute(f"UPDATE Customers SET active = 0 WHERE customerName = '{customer.name}'")


# print("largest customerID:")
# cursor.execute("SELECT MAX(customerID) FROM Customers")
# print(cursor.fetchall()[0][0])