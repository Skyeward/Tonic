from tools.tonic_generic import indexed_menu as i_menu
from tools.tonic_format import format_string as fmat
from tools.tonic_generic import get_valid_index, get_instance_variables, get_unique_string
from models.twitch_data import TwitchData as TwitchData

class Customer():
    def __init__(self):
        self.name = None
        self.favourite_drink = None


    def choose_name(self, existing_customers: ["Customer"], twitch_data, cancel_strings: [str] = ["", "cancel"]) -> str:
        "Continually asks for name from user until a unqiue name is given and saves to self.name; can optionally be given a list of strings which cancel the funtion (use lowercase). Returns the new name, or None if cancelled by user."
        
        unavailable_names = []
            
        for customer in existing_customers:
            unavailable_names.append(customer.name.lower())

        input_message = "Please type the customer's name:"
        fail_message = "This name is already in use. Please try a different name:"
        print(input_message + " (type 'cancel' to return to menu)")
        user_input = get_unique_string(twitch_data, unavailable_names, input_message, fail_message)
        #user_input = twitch_data.find_command("index")

        if user_input in cancel_strings or user_input == None:
            return None

        self.name = user_input.title()
        return self.name


    def choose_drink(self, drinks: ["Drink"], twitch_data) -> str:
        "Prints table of drinks and continually asks for an index selection. Saves to self.favourite_drink;  can optionally be given a list of strings which cancel the funtion (use lowercase). Returns the new name, or None if cancelled by user."

        drink_names = get_instance_variables(drinks, "name")
        print_table = i_menu({"": ["BACK"] + drink_names}, "CHOOSE A DRINK")

        for line in print_table:
            print(line)

        #chosen_index = get_valid_index(len(drink_names) + 1)
        chosen_index = twitch_data.find_command("index", number_of_options = len(drink_names) + 1)

        if chosen_index == 0:
            return None

        self.favourite_drink = drink_names[chosen_index - 1]
        return self.favourite_drink