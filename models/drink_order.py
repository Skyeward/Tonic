from datetime import datetime
from tools.tonic_generic import get_instance_variables

class DrinkOrder():
    def __init__(self):
        self.customers = []
        self.drinks = []
        self.time_placed = None
        self.runner = None


    def add_drink(self, customer, drink):
        self.customers.append(customer)
        self.drinks.append(drink)


    def remove_drink(self, customer):
        customer_names = get_instance_variables(self.customers, "name")
        customer_to_remove_index = customer_names.index(customer.name)

        self.customers.pop(customer_to_remove_index)
        self.drinks.pop(customer_to_remove_index)
    

    def set_placement_time(self):
        "Updates time_placed to the current time."
        self.time_placed = str(datetime.now()).split(".")[0]
        #splitting time at the decimal shaves off milliseconds which aren't needed