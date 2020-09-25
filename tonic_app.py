from tools.tonic_launch import intro as intro
from tools.tonic_generic import indexed_menu as i_menu, format_string as fmat
from tools.tonic_generic import get_valid_index, get_instance_variables, get_unique_string
from tools.tonic_saveload import json_save as _json_save, json_load as json_load
from models.customer import Customer as Customer
from models.drink_order import DrinkOrder as DrinkOrder
from models.drink import Drink as Drink

menu_options = {}
customers = []
available_drinks = []
order_history = []

save_data_path = "./data/tonic_data.json"
save_synced = True


def load():
    loaded_instances = json_load(save_data_path)

    if loaded_instances == None:
        return

    global_data_lists = {"Customer": customers, "Drink": available_drinks, "DrinkOrder": order_history}

    for instance in loaded_instances:
        type_as_string = type(instance).__name__
        global_data_lists[type_as_string].append(instance)


def populate_menu_options():
    "Adds all main menu options to the menu_options dictionary. Strings are keys, and function names are values."
    
    return_dict = {}
    
    return_dict["View Customers"] = view_customers
    return_dict["Add Customer"] = add_customer
    return_dict["Remove Customer"] = remove_customer
    return_dict["View Drinks"] = view_drinks
    return_dict["Add Drink"] = add_drink
    return_dict["Remove Drink"] = remove_drink
    # return_list.append([search, "Search"])
    # return_list.append([view_order_history, "View Order History"])
    return_dict["Place An Order"] = order_menu_loop
    # return_list.append([ask_order_from_template, "Place An Order"])
    # return_list.append([trains, "I Like Trains"])
    return_dict["Force Save Data"] = save
    return_dict["Exit App"] = exit_app

    return return_dict


def populate_order_menu_options():
    "Adds all order menu options to the order_menu_options dictionary. Strings are keys, and function names are values."

    return_dict = {}

    return_dict["Cancel Order"] = order_cancel
    return_dict["View Order"] = order_view
    return_dict["Choose Runner"] = order_choose_runner
    return_dict["Change Runner"] = order_choose_runner
    return_dict["Add Guest"] = order_new_customer
    return_dict["Add Drinks From Favourites"] = order_add_from_favourites
    return_dict["Remove Drink Selection"] = order_remove_drink
    return_dict["Confirm Order"] = order_confirm

    return return_dict


def save(): #(instances, new_data_name, new_data_name = "")
    is_success = _json_save(save_data_path, customers + available_drinks + order_history)
    global save_synced

    if is_success == True:
        print(f"Your data has been saved.")
        save_synced = True
    else:
        print(f"There was a problem saving your data. New data will be lost when the app is closed.")
        print("A Save Data option has been added to the main menu. Try saving your data again later.")
        save_synced = False


def view_customers():
    customer_names = get_instance_variables(customers, "name")
    customer_drinks = get_instance_variables(customers, "favourite_drink")
    drink_names = get_instance_variables(customer_drinks, "name")
    
    print_menu = i_menu({"NAME": customer_names, "FAVOURITE DRINK": drink_names}, "CUSTOMERS", True)

    for line in print_menu:
        print(line)


def add_customer():
    new_customer = new_customer_instance(customers)

    if new_customer != None:
        customers.append(new_customer)
        save()


def new_customer_instance(customers_to_check_against):
    new_customer = Customer()
    new_name = new_customer.choose_name(customers_to_check_against)

    if new_name == None:
        return None

    print()
    new_drink = new_customer.choose_drink(available_drinks)

    if new_drink == None:
        return None

    return new_customer


def remove_customer():
    customer_names = ["BACK"]
    customer_drinks = [""]
    customer_names += get_instance_variables(customers, "name")
    customer_drinks += get_instance_variables(get_instance_variables(customers, "favourite_drink"), "name")

    customer_table = i_menu({"CUSTOMER": customer_names, "DRINK": customer_drinks}, "CHOOSE CUSTOMER TO REMOVE", True)

    for line in customer_table:
        print(line)

    chosen_index = get_valid_index(len(customer_names) + 1)

    if chosen_index == 0:
        return
    
    customer_to_remove = customers[chosen_index - 1]
    customers.remove(customer_to_remove)
    save()


def view_drinks():
    drink_names = get_instance_variables(available_drinks, "name")

    print_menu = i_menu({"": drink_names}, "DRINKS")

    for line in print_menu:
        print(line)


def add_drink():
    new_drink = Drink()
    new_name = new_drink.choose_name(available_drinks)

    if new_name == None:
        return None
    
    available_drinks.append(new_drink)
    save()
    return new_drink #required for testing


def remove_drink():
    drinks = get_instance_variables(available_drinks, "name")

    drinks_table = i_menu({"": ["BACK"] + drinks}, "CHOOSE DRINK TO REMOVE")

    for line in drinks_table:
        print(line)

    chosen_index = get_valid_index(len(drinks) + 1)

    if chosen_index == 0:
        return
    
    drink_to_remove = available_drinks[chosen_index - 1]
    available_drinks.remove(drink_to_remove)
    save()


def order_menu_loop(new_order = None):
    "Menu to make a new order, and is recursively run until order is cancelled or confirmed."

    if new_order == None:
        new_order = DrinkOrder()

    print()
    
    #ADDS OPTION STRINGS TO options_to_print AND REMOVES SOME OPTIONS UNDER SPECIFIC CONDITIONS
    options_to_print = list(order_menu_options.keys())

    if new_order.runner == None:
        options_to_print.remove("Change Runner")
    else:
        options_to_print.remove("Choose Runner")

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
    
    menu_to_print = i_menu({subheader: options_to_print}, f"ORDER OPTIONS - {len(new_order.customers)} DRINKS ADDED", True)
    
    for line in menu_to_print:
        print(line)

    chosen_index = get_valid_index(len(options_to_print))
    chosen_option = options_to_print[chosen_index]
    is_loop = order_menu_options[chosen_option](new_order)

    #LOOPS MENU UNLESS order_cancel() or order_confirm() WAS RUN (AND APPENDS order_history IN THE LATTER CASE)
    if is_loop == True:
        order_menu_loop(new_order)


def order_cancel(order): #order not required for this function, but is passed to all order functions
    confirm_table = i_menu({"": ["No", "Yes"]}, "CANCEL ORDER?")

    for line in confirm_table:
        print(line)

    chosen_index = get_valid_index(2)

    if chosen_index == 0:
        return True
    else:
        return False


def order_view(order):
    customer_names = get_instance_variables(order.customers, "name")
    drink_names = get_instance_variables(order.drinks, "name")

    print_menu = i_menu({"CUSTOMER": customer_names, "DRINK": drink_names}, "CURRENT ORDER", True)
    
    for line in print_menu:
        print(line)
            
    print()
    return True


def order_choose_runner(order, change_string = "CHOOSE"):
    names = get_instance_variables(customers, "name")
    names_table = i_menu({"": ["CANCEL"] + names}, "CHOOSE RUNNER")

    for line in names_table:
        print(line)

    chosen_index = get_valid_index(len(names) + 1)

    if chosen_index == 0:
        print("Cancelling...\n")
        return True

    runner = customers[chosen_index - 1]
    order.runner = runner
    return True


def order_new_customer(order):
    new_customer = new_customer_instance(order.customers)

    if new_customer == None:
        print("Cancelling...\n")
        return True
    
    order.add_drink(new_customer, new_customer.favourite_drink)
    return True


def order_remove_drink(order):
    order_customers = ["CANCEL"] + get_instance_variables(order.customers, "name")
    order_drinks = [""] + get_instance_variables(order.drinks, "name")

    print_menu = i_menu({"CUSTOMERS": order_customers, "DRINKS": order_drinks}, "CHOOSE DRINK TO REMOVE", True)

    for line in print_menu:
        print(line)

    chosen_index = get_valid_index(len(order_customers))

    if chosen_index == 0:
        print("Cancelling...\n")
        return True

    order.remove_drink(order.customers[chosen_index - 1])
    return True


def order_add_from_favourites(order):
    saved_customers = customers.copy()
    saved_customer_names = get_instance_variables(customers, "name")
    order_customer_names = get_instance_variables(order.customers, "name")

    for i, name in enumerate(saved_customer_names):
        if name in order_customer_names:
            saved_customers.pop(i)
            saved_customer_names.pop(i)
    
    saved_customer_drinks = get_instance_variables(saved_customers, "favourite_drink")
    saved_customer_drinks_names = get_instance_variables(saved_customer_drinks, "name")

    print_menu = i_menu({"CUSTOMER": ["DONE"] + saved_customer_names, "DRINK": [""] + saved_customer_drinks_names}, "ADD DRINK", True)

    for line in print_menu:
        print(line)

    chosen_index = get_valid_index(len(saved_customer_names) + 1)

    if chosen_index != 0:
        order.add_drink(saved_customers[chosen_index - 1], saved_customer_drinks[chosen_index - 1])

    if chosen_index == 0 or len(saved_customer_names) == 1:
        return True

    return order_add_from_favourites(order)


def order_confirm(order):
    confirm_table = i_menu({"": ["No", "Yes"]}, "CONFIRM ORDER?")

    for line in confirm_table:
        print(line)

    chosen_index = get_valid_index(2)

    if chosen_index == 0:
        return True
    else:
        order_history.append(order)
        return False


def exit_app():
    print("Exiting App...")
    

def main_menu_loop():
    "Menu which serves as the root of the app, and is recursively run until app is exited."

    print()

    #ADDS OPTION STRINGS TO options_to_print AND REMOVES SOME OPTIONS UNDER SPECIFIC CONDITIONS
    options_to_print = list(menu_options.keys())

    if save_synced == True:
        options_to_print.remove("Force Save Data")
    
    if len(customers) == 0:
        options_to_print.remove("Remove Customer")
        options_to_print.remove("View Customers")

    if len(available_drinks) == 0:
        options_to_print.remove("Add Customer")
        options_to_print.remove("Remove Drink")
        options_to_print.remove("View Drinks")
        options_to_print.remove("Place An Order")
        print("Your list of available drinks is currently empty. I recommend starting with the Add Drink option!")
        print()

    #PRINTS MAIN MENU, GETS USER CHOICE AND RUNS FUNCTION
    menu_to_print = i_menu({"": options_to_print}, "WELCOME TO TONIC!")
    
    for line in menu_to_print:
        print(line)

    chosen_index = get_valid_index(len(options_to_print))
    chosen_option = options_to_print[chosen_index]
    menu_options[chosen_option]()

    #LOOPS MENU UNLESS exit_app() WAS RUN
    if menu_options[chosen_option] != exit_app:
        main_menu_loop()


if __name__ == "__main__":
    load()
    menu_options = populate_menu_options()
    order_menu_options = populate_order_menu_options()
    print(intro())
    main_menu_loop()