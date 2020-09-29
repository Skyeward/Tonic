class MenuData():
    def __init__(self):
        self.menu_options = {}
        self.order_menu_options = {}
        self._populate_menu_options()
        self._populate_order_menu_options()

    
    def _populate_menu_options(self):
        self.menu_options["View Customers"] = "view_customers"
        self.menu_options["Add Customer"] = "add_customer"
        self.menu_options["Remove Customer"] = "remove_customer"
        self.menu_options["View Drinks"] = "view_drinks"
        self.menu_options["Add Drink"] = "add_drink"
        self.menu_options["Remove Drink"] = "remove_drink"
        self.menu_options["Search"] = "search"
        self.menu_options["View Order History"] = "view_order_history"
        # return_list.append([view_order_history, "View Order History"])
        self.menu_options["Place An Order"] = "order_menu_loop"
        # return_list.append([ask_order_from_template, "Place An Order"])
        # return_list.append([trains, "I Like Trains"])
        self.menu_options["Force Save Data"] = "save"
        self.menu_options["Exit App"] = "exit_app"


    def _populate_order_menu_options(self):
        self.order_menu_options["Cancel Order"] = "order_cancel"
        self.order_menu_options["View Order"] = "order_view"
        self.order_menu_options["Choose Runner"] = "order_choose_runner"
        self.order_menu_options["Change Runner"] = "order_choose_runner"
        self.order_menu_options["Add Guest"] = "order_new_customer"
        self.order_menu_options["Add Drinks From Favourites"] = "order_add_from_favourites"
        self.order_menu_options["Remove Drink Selection"] = "order_remove_drink"
        self.order_menu_options["Confirm Order"] = "order_confirm"