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


def get_all_orders(cursor):
    cursor.execute(f"SELECT orderID, runner, timePlaced FROM Orders")
    results = cursor.fetchall()

    order_dict = {}

    for order_data in results:
        order = DrinkOrder()
        runner = Customer()

        runner.name = order_data[1]
        order.runner = runner
        order.time_placed = str(order_data[2])

        order_dict[order_data[0]] = order

    cursor.execute(f"SELECT orderID, customerName, drinkName FROM OrderRequests")
    results = cursor.fetchall()

    for customer_data in results:
        customer = Customer()

        customer.name = customer_data[1]
        customer.favourite_drink = customer_data[2]

        order_dict[customer_data[0]].customers.append(customer)

    return list(order_dict.values())


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


def add_order(cursor, order):
    cursor.execute(f"INSERT INTO Orders (runner) VALUES ('{order.runner.name}')")
    cursor.execute("SELECT MAX(orderID) FROM Orders")
    order_ID = cursor.fetchall()[0][0]

    for customer in order.customers:
        cursor.execute(f"INSERT INTO OrderRequests (orderID, customerName, drinkName) VALUES ({order_ID}, '{customer.name}', '{customer.favourite_drink}')")