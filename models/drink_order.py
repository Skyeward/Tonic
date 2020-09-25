from datetime import datetime

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
        pass
    

    def set_placement_time(self):
        "Updates time_placed to the current time."
        self.time_placed = str(datetime.now()).split(".")[0]
        #splitting time at the decimal shaves off milliseconds which aren't needed