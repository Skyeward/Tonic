from tools.tonic_generic import get_unique_string

class Drink():
    def __init__(self):
        self.name = None

    
    def choose_name(self, existing_drinks: ["Drink"], cancel_strings: [str] = ["", "cancel"]) -> str:
        "Shows available drinks asks for drink from user until a unqiue name is given and saves to self.name; can optionally be given a list of strings which cancel the funtion (use lowercase). Returns the new name, or None if cancelled by user."

        unavailable_drinks = []
            
        for drink in existing_drinks:
            unavailable_drinks.append(drink.name.lower())

        input_message = "Please type the name of the new drink:"
        fail_message = "This drink has already been added. Please try a different drink:"
        user_input = get_unique_string(unavailable_drinks, input_message, fail_message)

        self.name = user_input
        return self.name