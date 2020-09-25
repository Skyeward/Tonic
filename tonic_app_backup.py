import tonic_launch as launch
from tonic_generic import indexed_menu as i_menu, format_string as fmat
from tonic_generic import get_valid_index, get_instance_variables, get_unique_string
#from ../models/customer import Customer as Customer

menu_options = {}
customers = []
available_drinks = []
order_history = []


class Customer():
    def __init__(self):
        self.name = None
        self.favourite_drink = None


    def choose_name(self, existing_customers: ["Customer"], cancel_strings: [str] = ["", "cancel"]) -> str:
        "Continually asks for name from user until a unqiue name is given and saves to self.name; can optionally be given a list of strings which cancel the funtion (use lowercase). Returns the new name, or None if cancelled by user."
        
        unavailable_names = []
            
        for customer in existing_customers:
            unavailable_names.append(customer.name.lower())

        input_message = "Please type the customer's name:"
        fail_message = "This name is already in use. Please try a different name:"
        user_input = get_unique_string(unavailable_names, input_message, fail_message)

        self.name = user_input.title()
        return self.name


class Drink():
    def __init__(self):
        self.name = None

    
    def choose_name(self, existing_drinks: ["Drink"], cancel_strings: [str] = ["", "cancel"]) -> str:
        "Continually asks for name from user until a unqiue name is given and saves to self.name; can optionally be given a list of strings which cancel the funtion (use lowercase). Returns the new name, or None if cancelled by user."

        unavailable_drinks = []
            
        for drink in existing_drinks:
            unavailable_drinks.append(drink.name.lower())

        input_message = "Please type the name of the new drink:"
        fail_message = "This drink has already been added. Please try a different drink:"
        user_input = get_unique_string(unavailable_drinks, input_message, fail_message)

        self.name = user_input
        return self.name


def populate_menu_options():
    "Adds all main menu options to the menu_options dictionary. Strings are keys, and function names are values."
    
    return_dict = {}
    
    # return_list.append([get_customers_and_drinks, "View Customers"])
    return_dict["Add Customer"] = add_customer
    return_dict["Remove Customer"] = remove_customer
    # return_list.append([get_drinks, "View Drinks"])
    # return_list.append([add_drink, "Add Drink"])
    # return_list.append([remove_drink, "Remove Drink"])
    # return_list.append([search, "Search"])
    # return_list.append([view_order_history, "View Order History"])
    # return_list.append([ask_order_from_template, "Place An Order"])
    # return_list.append([trains, "I Like Trains"])
    return_dict["Exit App"] = exit_app

    return return_dict


def add_customer():
    new_customer = Customer()
    new_name = new_customer.choose_name(customers)

    if new_name == None:
        return

    new_drink = new_customer.choose_drink(available_drinks)

    if new_drink == None:
        return
    
    customers.append(new_customer)
    print(f"{new_name} has been added.")


def remove_customer():
    customer_names = ["BACK"]
    customer_drinks = [""]
    customer_names += get_instance_variables(customers, "name")
    customer_drinks += get_instance_variables(customers, "favourite_drink")

    customer_table = i_menu({"CUSTOMER": customer_names, "DRINK": customer_drinks}, "CHOOSE CUSTOMER TO REMOVE", True)

    for line in customer_table:
        print(line)

    chosen_index = get_valid_index(len(customer_names) + 1)

    if chosen_index == 0:
        return
    
    customer_to_remove = customers[chosen_index - 1]
    customers.remove(customer_to_remove)
    print(f"You have successfully removed {customer_to_remove.name}")
    

def exit_app():
    print("Exiting App...")
    

def main_menu_loop():
    "Menu which serves as the root of the app, and is recursively run until app is exited."

    new_customer = Customer()
    
    #ADDS OPTION STRINGS TO options_to_print AND REMOVES SOME OPTIONS UNDER SPECIFIC CONDITIONS
    options_to_print = list(menu_options.keys())

    if len(customers) == 0:
        options_to_print.remove("Remove Customer")

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
    menu_options = populate_menu_options()
    
    print(launch.intro())
    print()

    if len(available_drinks) == 0:
        print("Your list of available drinks is currently empty. I recommend starting with the Add Drink option!")
        print() 

    main_menu_loop()

# menu_to_print = i_menu({"BREEDS OF DOG": ("poodle", "pug", "boxer", "shiba inu"), "FRUIT": ["watermelon", "pear", "apple", "grape", "banana", "lemon", "kiwi", "pineapple", "raspberry", "peach", "plum", "mango"]}, "DOGS AND FRUIT", True)