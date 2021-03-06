from random import randrange as randrange
from tools.tonic_launch import intro as intro
from tools.tonic_generic import indexed_menu as i_menu, format_string as fmat
from tools.tonic_generic import get_valid_index, get_instance_variables
from tools.tonic_generic import get_unique_string, print_table_get_index
from models.customer import Customer as Customer
from models.drink_order import DrinkOrder as DrinkOrder
from models.drink import Drink as Drink
from models.menu_data import MenuData as MenuData
import pymysql as sql
import tools.tonic_sql as sql
from tools.tonic_sql import sql_connect_wrapper as db

from datetime import datetime


def load():
    customers = db(sql.get_all_customers)
    drinks = db(sql.get_all_drinks)
    orders = db(sql.get_all_orders)

    return (customers, drinks, orders)


def view_customers(**kwargs): 
    customer_names = get_instance_variables(kwargs["customers"], "name")
    drink_names = get_instance_variables(kwargs["customers"], "favourite_drink")
    
    print_menu = i_menu({"NAME": customer_names, "FAVOURITE DRINK": drink_names}, "CUSTOMERS", True)

    for line in print_menu:
        print(line)


def add_customer(**kwargs):
    new_customer = _new_customer_instance(**kwargs)

    if new_customer == None:
        return

    db(sql.add_customer, new_customer)
    kwargs["customers"].append(new_customer)


def _new_customer_instance(**kwargs):
    new_customer = Customer()
    new_name = new_customer.choose_name(kwargs["customers"])

    if new_name == None:
        return None

    print()
    new_drink = new_customer.choose_drink(kwargs["drinks"])

    if new_drink == None:
        return None

    return new_customer


def remove_customer(**kwargs):
    customer_names = ["BACK"]
    customer_drinks = [""]
    customer_names += get_instance_variables(kwargs["customers"], "name")
    customer_drinks += get_instance_variables(kwargs["customers"], "favourite_drink")

    chosen_index = print_table_get_index({"CUSTOMER": customer_names, "DRINK": customer_drinks}, "CHOOSE CUSTOMER TO REMOVE", True)

    if chosen_index == 0:
        return
    
    customer_to_remove = kwargs["customers"][chosen_index - 1]
    db(sql.remove_customer, customer_to_remove)
    customers.remove(customer_to_remove)


def view_drinks(**kwargs):
    drink_names = get_instance_variables(kwargs["drinks"], "name")
    print_menu = i_menu({"": drink_names}, "DRINKS")

    for line in print_menu:
        print(line)


def add_drink(**kwargs):
    new_drink = Drink()
    new_name = new_drink.choose_name(kwargs["drinks"])

    if new_name == None:
        return None

    db(sql.add_drink, new_drink)
    kwargs["drinks"].append(new_drink)
    return new_drink #required for testing


def remove_drink(**kwargs):
    drinks = get_instance_variables(kwargs["drinks"], "name")
    chosen_index = print_table_get_index({"": ["BACK"] + drinks}, "CHOOSE DRINK TO REMOVE")

    if chosen_index == 0:
        return

    drink_to_remove = kwargs["drinks"][chosen_index - 1]
    db(sql.remove_drink, drink_to_remove)
    kwargs["drinks"].remove(drink_to_remove)


def search(**kwargs):
    search_query = input("Search for a name or drink. (Type 'cancel' to return to the Main Menu.)\n>>> ").lower()
    print()

    if search_query == "" or search_query == "cancel":
        return

    customer_names = get_instance_variables(kwargs["customers"], "name")
    drink_names = get_instance_variables(kwargs["drinks"], "name")
    search_results = {}
    exact_results = {}

    for customer in customer_names:
        customer = customer.lower()

        if search_query in customer:
            if customer == search_query:
                exact_results[customer.title()] = "customer"
            else:
                search_results[customer.title()] = "customer"
        
    for drink in drink_names:
        drink = drink.lower()
        
        if search_query in drink:
            if drink == search_query:
                exact_results[drink] = "drink"
            else:
                search_results[drink] = "drink"
    
    if len(search_results) + len(exact_results) == 0:
        print("No matches found.")
        _search_again()
        return

    name_column = []
    type_column = []
    
    for result, category in exact_results.items():
        name_column.append(result)
        type_column.append(category)
    
    non_exact_names = sorted(search_results.keys())
    
    for name in non_exact_names:
        name_column.append(name)

        if name in customer_names:
            type_column.append("customer")
        else:
            type_column.append("drink")

    print_menu = i_menu({"RESULT": name_column, "DATA TYPE": type_column}, "SEARCH RESULTS", True)

    for line in print_menu:
        print(line)

    _search_again(**kwargs)


def _search_again(**kwargs):
    chosen_index = print_table_get_index({"": ["No", "Yes"]}, "SEARCH AGAIN?")

    if chosen_index == 1:
        search(**kwargs)


def view_order_history(is_selecting_order = False, **kwargs):
    times = get_instance_variables(kwargs["orders"], "time_placed")
    runners = get_instance_variables(kwargs["orders"], "runner")
    runner_names = get_instance_variables(runners, "name")
    customer_lists = get_instance_variables(kwargs["orders"], "customers")
    customer_counts = []

    for list_ in customer_lists:
        customer_counts.append(f"{len(list_)} drinks")

    chosen_index = print_table_get_index({"DATE": ["BACK"] + times, "RUNNER": [""] + runner_names, "ORDER SIZE": [""] + customer_counts}, "PREVIOUS ORDERS", True)

    if chosen_index == 0:
        return None

    chosen_order = kwargs["orders"][chosen_index - 1]
    yes_or_no = view_previous_order(chosen_order, is_selecting_order)

    if yes_or_no == None:
        return None
    elif yes_or_no == 0:
        return view_order_history(is_selecting_order, **kwargs)
    else:
        return chosen_order


def view_previous_order(order, is_selecting_order):
    customer_names = get_instance_variables(order.customers, "name")
    customer_drinks = get_instance_variables(order.customers, "favourite_drink")

    if is_selecting_order == True:
        customer_names.insert(0, "BACK")
        customer_drinks.insert(0, "")

    print_table = i_menu({"CUSTOMER": customer_names, "DRINK": customer_drinks}, f"ORDER PLACED {order.time_placed}", True)

    for line in print_table:
        print(line)
    
    if is_selecting_order == False:
        return None

    yes_or_no = print_table_get_index({"": ["No", "Yes"]}, "START WITH COPY OF THIS ORDER?")
    return yes_or_no
    

def question_user_before_order(menu_data, customers, drinks, orders):
    if len(orders) == 0:
        order_menu_loop(menu_data, customers, drinks, orders)
        return
    
    yes_or_no = print_table_get_index({"": ["No", "Yes"]}, "START WITH COPY OF PREVIOUS ORDER?")

    if yes_or_no == 0:
        order_menu_loop(menu_data, customers, drinks, orders)
        return
    else:
        chosen_order = view_order_history(True, orders = orders)

    if chosen_order == None:
        order_menu_loop(menu_data, customers, drinks, orders)
    else:
        order_menu_loop(menu_data, customers, drinks, orders, chosen_order)


def order_menu_loop(menu_data, customers, drinks, orders, new_order = None):
    "Menu to make a new order, and is recursively run until order is cancelled or confirmed."

    if new_order == None:
        new_order = DrinkOrder()

    print()
    
    #ADDS OPTION STRINGS TO options_to_print AND REMOVES SOME OPTIONS UNDER SPECIFIC CONDITIONS
    options_to_print = list(menu_data.order_menu_options.keys())

    if new_order.runner == None:
        options_to_print.remove("Change Runner")
    else:
        options_to_print.remove("Choose Runner")

    if len(customers) == 0:
        options_to_print.remove("Add Drinks From Favourites")

    if len(new_order.customers) == 0:
        options_to_print.remove("Remove Drink Selection")
        options_to_print.remove("Edit Customer's Drink")
        options_to_print.remove("View Order")

    if new_order.runner == None or len(new_order.customers) == 0:
        options_to_print.remove("Confirm Order")

    #PRINTS ORDER MENU, GETS USER CHOICE AND RUNS FUNCTION
    if new_order.runner == None:
        subheader = "NO RUNNER CHOSEN"
    else:
        subheader = f"{new_order.runner.name.upper()}'S DRINKS RUN"
    
    chosen_index = print_table_get_index({subheader: options_to_print}, f"ORDER OPTIONS - {len(new_order.customers)} DRINKS ADDED", True)
    chosen_option = options_to_print[chosen_index]
    chosen_function = menu_data.order_menu_options[chosen_option]
    is_loop = eval(chosen_function)(new_order, customers = customers, drinks = drinks, orders = orders, menu_data = menu_data)

    #LOOPS MENU UNLESS order_cancel() or order_confirm() WAS RUN (AND APPENDS order_history IN THE LATTER CASE)
    if is_loop == True:
        order_menu_loop(menu_data, customers, drinks, orders, new_order)


def order_cancel(order, **kwargs): #order not required for this function, but is passed to all order functions
    chosen_index = print_table_get_index({"": ["No", "Yes"]}, "CANCEL ORDER?")

    if chosen_index == 0:
        return True
    else:
        return False


def order_view(order, **kwargs):
    customer_names = get_instance_variables(order.customers, "name")
    drink_names = get_instance_variables(order.customers, "favourite_drink")

    print_menu = i_menu({"CUSTOMER": customer_names, "DRINK": drink_names}, "CURRENT ORDER", True)
    
    for line in print_menu:
        print(line)
            
    print()
    return True


def order_choose_runner(order, **kwargs):
    names = get_instance_variables(kwargs["customers"], "name")
    chosen_index = print_table_get_index({"": ["CANCEL"] + names}, "CHOOSE RUNNER")

    if chosen_index == 0:
        print("Cancelling...\n")
        return True

    runner = customers[chosen_index - 1]
    order.runner = runner
    return True


def order_new_customer(order, **kwargs):
    new_customer = _new_customer_instance(customers = order.customers, drinks = kwargs["drinks"])

    if new_customer == None:
        print("Cancelling...\n")
        return True
    
    order.customers.append(new_customer)
    return True


def order_remove_drink(order, **kwargs):
    chosen_index = _get_order_drink_index(order)

    if chosen_index == 0:
        print("Cancelling...\n")
        return True

    order.remove_drink(order.customers[chosen_index - 1])
    return True


def order_edit_drink(order, **kwargs):
    chosen_customer_index = _get_order_drink_index(order)

    if chosen_customer_index == 0:
        print("Cancelling...\n")
        return True

    customer_name = order.customers[chosen_customer_index - 1].name
    drink_names = get_instance_variables(kwargs["drinks"], "name")
    chosen_drink_index = print_table_get_index({"": ["CANCEL"] + drink_names}, f"CHOOSE {customer_name.upper()}'S DRINK")

    if chosen_drink_index == 0:
        print("Cancelling...\n")
        return True

    drink_name = drink_names[chosen_drink_index - 1]
    order.customers[chosen_customer_index - 1].favourite_drink = drink_name
    
    return True


def _get_order_drink_index(order):
    order_customers = ["CANCEL"] + get_instance_variables(order.customers, "name")
    order_drinks = [""] + get_instance_variables(order.customers, "favourite_drink")
    return print_table_get_index({"CUSTOMERS": order_customers, "DRINKS": order_drinks}, "CHOOSE DRINK TO REMOVE", True)
    

#TODO: Disallow when empty
def order_add_from_favourites(order, **kwargs):
    names_in_order = get_instance_variables(order.customers, "name")
    available_customers = []

    for customer in kwargs["customers"]:
        if customer.name not in names_in_order:
            available_customers.append(customer)
    
    available_customer_names = get_instance_variables(available_customers, "name")
    available_drink_names = get_instance_variables(available_customers, "favourite_drink")
    chosen_index = print_table_get_index({"CUSTOMER": ["DONE"] + available_customer_names, "DRINK": [""] + available_drink_names}, "ADD DRINK", True)

    if chosen_index != 0:
        order.customers.append(available_customers[chosen_index - 1])

    if chosen_index == 0 or len(available_customers) == 1:
        return True

    return order_add_from_favourites(order, **kwargs)


def order_random_suggestion(order, **kwargs):
    messages = kwargs["menu_data"].random_drink_messages
    message_count = len(messages)
    random_message = messages[randrange(0, message_count)]

    drinks = kwargs["drinks"]
    drinks_count = len(drinks)
    random_drink = drinks[randrange(0, drinks_count)].name

    random_message = random_message.replace("#", random_drink)

    if random_drink[0] in "aeiou":
        drink_starts_with_vowel = True
    else:
        drink_starts_with_vowel = False

    determiner = "a" + ("n" * int(drink_starts_with_vowel))
    random_message = random_message.replace("@", f"{determiner} {random_drink}")

    print(random_message)
    return True


def order_confirm(order, **kwargs):
    chosen_index = print_table_get_index({"": ["No", "Yes"]}, "CONFIRM ORDER?")

    if chosen_index == 0:
        return True
    else:
        order.time_placed = str(datetime.utcnow()).split(".")[0]
        kwargs["customers"].append(order)
        db(sql.add_order, order)
        return False


def exit_app(**kwargs):
    print("Exiting App...")
    

def main_menu_loop(menu_data, customers, drinks, orders):
    "Menu which serves as the root of the app, and is recursively run until app is exited."

    print()

    #ADDS OPTION STRINGS TO options_to_print AND REMOVES SOME OPTIONS UNDER SPECIFIC CONDITIONS
    options_to_print = list(menu_data.menu_options.keys())
    
    if len(customers) == 0:
        options_to_print.remove("Remove Customer")
        options_to_print.remove("View Customers")
        options_to_print.remove("Place An Order")

    if len(orders) == 0:
        options_to_print.remove("View Order History")

    if len(drinks) == 0:
        if "Place An Order" in options_to_print:
            options_to_print.remove("Place An Order")

        options_to_print.remove("Add Customer")
        options_to_print.remove("Remove Drink")
        options_to_print.remove("View Drinks")
        print("Your list of available drinks is currently empty. I recommend starting with the Add Drink option!")
        print()

    #PRINTS MAIN MENU, GETS USER CHOICE AND RUNS FUNCTION
    chosen_index = print_table_get_index({"": options_to_print}, "WELCOME TO TONIC!")
    chosen_option = options_to_print[chosen_index]
    chosen_function = menu_data.menu_options[chosen_option]

    if chosen_function == "question_user_before_order":
        question_user_before_order(menu_data, customers, drinks, orders)
    else:
        eval(chosen_function)(customers = customers, drinks = drinks, orders = orders)

    #LOOPS MENU UNLESS exit_app() WAS RUN
    if menu_data.menu_options[chosen_option] != "exit_app":
        main_menu_loop(menu_data, customers, drinks, orders)


if __name__ == "__main__":  
    customers, drinks, orders = load()
    menu_data = MenuData()
    print(intro())
    main_menu_loop(menu_data, customers, drinks, orders)