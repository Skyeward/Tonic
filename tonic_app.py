from tools.tonic_launch import intro as intro
from tools.tonic_generic import indexed_menu as i_menu, format_string as fmat
from tools.tonic_generic import get_valid_index, get_instance_variables
from tools.tonic_generic import get_unique_string, print_table_get_index
from tools.tonic_saveload import json_save as _json_save, json_load as json_load
from models.customer import Customer as Customer
from models.drink_order import DrinkOrder as DrinkOrder
from models.drink import Drink as Drink
from models.menu_data import MenuData as MenuData
import pymysql as sql
import tools.tonic_sql as sql
from tools.tonic_sql import sql_connect_wrapper as db


customers = []
available_drinks = []
order_history = []

save_data_path = "./data/tonic_data.json"
save_synced = True


def load():
    customers = db(sql.get_all_customers)
    drinks = db(sql.get_all_drinks)

    return (customers, drinks)


def save():
    is_success = _json_save(save_data_path, customers + available_drinks + order_history)
    global save_synced

    if is_success == True:
        print(f"Your data has been saved.")
        save_synced = True
    else:
        print(f"There was a problem saving your data. New data will be lost when the app is closed.")
        print("A Save Data option has been added to the main menu. Try saving your data again later.")
        save_synced = False


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
    save()


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


def view_order_history(is_selecting_order = False):
    times = get_instance_variables(order_history, "time_placed")
    runners = get_instance_variables(order_history, "runner")
    runner_names = get_instance_variables(runners, "name")
    customer_lists = get_instance_variables(order_history, "customers")
    customer_counts = []

    for list_ in customer_lists:
        print(list_)
        customer_counts.append(f"{len(list_)} drinks")

    chosen_index = print_table_get_index({"DATE": ["BACK"] + times, "RUNNER": [""] + runner_names, "ORDER SIZE": [""] + customer_counts}, "PREVIOUS ORDERS", True)

    if chosen_index == 0:
        return None

    chosen_order = order_history[chosen_index - 1]
    return view_previous_order(chosen_order, is_selecting_order)


def view_previous_order(order, is_selecting_order):
    customer_names = get_instance_variables(order.customers, "name")
    customer_drinks = get_instance_variables(order.customers, "favourite_drink")
    drink_names = get_instance_variables(customer_drinks, "name")

    if is_selecting_order == True:
        customer_names.insert(0, "BACK")
        drink_names.insert(0, "")

    print_table = i_menu({"CUSTOMER": customer_names, "DRINK": drink_names}, f"ORDER PLACED {order.time_placed}", True)

    for line in print_table:
        print(line)
    
    if is_selecting_order == False:
        return None

    chosen_index = get_valid_index(len(customer_names))
    return chosen_index
    

def question_user_before_order(menu_data, customers, drinks, orders):
    if len(orders) == 0:
        order_menu_loop(menu_data, customers, drinks, orders)
        return
    
    yes_or_no = print_table_get_index({"": ["No", "Yes"]}, "START WITH COPY OF PREVIOUS ORDER?")

    if yes_or_no == 0:
        order_menu_loop(menu_data, customers, drinks, orders)
        return
    else:
        chosen_order = view_order_history(True)

    if chosen_order == 0:
        question_user_before_order(menu_data, customers, drinks, orders)
    else:
        order = orders[chosen_order - 1].copy()
        order_menu_loop(menu_data, customers, drinks, orders, order)


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
    is_loop = eval(chosen_function)(new_order, customers = customers, drinks = drinks, orders = orders)

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

    # customer_names = order.customers
    # drink_names = order.drinks

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
    order_customers = ["CANCEL"] + get_instance_variables(order.customers, "name")
    order_drinks = [""] + get_instance_variables(order.drinks, "name")
    chosen_index = print_table_get_index({"CUSTOMERS": order_customers, "DRINKS": order_drinks}, "CHOOSE DRINK TO REMOVE", True)

    if chosen_index == 0:
        print("Cancelling...\n")
        return True

    order.remove_drink(order.customers[chosen_index - 1])
    return True
    

#TODO: Disallow when empty
def order_add_from_favourites(order, **kwargs):
    saved_customers = kwargs["customers"].copy()
    saved_customer_names = get_instance_variables(saved_customers, "name")
    order_customer_names = get_instance_variables(order.customers, "name")

    for i, name in enumerate(saved_customer_names):
        if name in order_customer_names:
            saved_customers.pop(i)
            saved_customer_names.pop(i)
    
    saved_customer_drinks_names = get_instance_variables(saved_customers, "favourite_drink")
    chosen_index = print_table_get_index({"CUSTOMER": ["DONE"] + saved_customer_names, "DRINK": [""] + saved_customer_drinks_names}, "ADD DRINK", True)

    if chosen_index != 0:
        order.customers.append(saved_customers[chosen_index - 1])

    if chosen_index == 0 or len(saved_customer_names) == 1:
        return True

    return order_add_from_favourites(order, **kwargs)


def order_confirm(order, **kwargs):
    chosen_index = print_table_get_index({"": ["No", "Yes"]}, "CONFIRM ORDER?")

    if chosen_index == 0:
        return True
    else:
        order.set_placement_time()
        order_history.append(order)
        #save()
        return False


def exit_app(**kwargs):
    print("Exiting App...")
    

def main_menu_loop(menu_data, customers, drinks, orders):
    "Menu which serves as the root of the app, and is recursively run until app is exited."

    print()

    #ADDS OPTION STRINGS TO options_to_print AND REMOVES SOME OPTIONS UNDER SPECIFIC CONDITIONS
    options_to_print = list(menu_data.menu_options.keys())

    if save_synced == True:
        options_to_print.remove("Force Save Data")
    
    if len(customers) == 0:
        options_to_print.remove("Remove Customer")
        options_to_print.remove("View Customers")
        options_to_print.remove("Place An Order")

    if len(order_history) == 0:
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
    customers, drinks = load()
    orders = [] #NEEDS CHANGING
    menu_data = MenuData()
    print(intro())
    main_menu_loop(menu_data, customers, drinks, orders)