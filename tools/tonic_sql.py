import pymysql as sql


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
