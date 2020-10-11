class MenuData():
    def __init__(self):
        self.menu_options = {}
        self.order_menu_options = {}
        self.random_drink_messages = []
        self._populate_menu_options()
        self._populate_order_menu_options()
        self._populate_random_drink_suggestions()

    
    def _populate_menu_options(self):
        self.menu_options["Find New App User"] = "switch_user"
        self.menu_options["View Customers"] = "view_customers"
        self.menu_options["Add Customer"] = "add_customer"
        self.menu_options["Remove Customer"] = "remove_customer"
        self.menu_options["View Drinks"] = "view_drinks"
        self.menu_options["Add Drink"] = "add_drink"
        self.menu_options["Remove Drink"] = "remove_drink"
        self.menu_options["Search"] = "search"
        self.menu_options["View Order History"] = "view_order_history"
        self.menu_options["Place An Order"] = "question_user_before_order"
        self.menu_options["Exit App"] = "exit_app"


    def _populate_order_menu_options(self):
        self.order_menu_options["Cancel Order"] = "order_cancel"
        self.order_menu_options["View Order"] = "order_view"
        self.order_menu_options["Choose Runner"] = "order_choose_runner"
        self.order_menu_options["Change Runner"] = "order_choose_runner"
        self.order_menu_options["Add Guest"] = "order_new_customer"
        self.order_menu_options["Add Drinks From Favourites"] = "order_add_from_favourites"
        self.order_menu_options["Add Drinks From Twitch!"] = "order_twitch"
        self.order_menu_options["Edit Customer's Drink"] = "order_edit_drink"
        self.order_menu_options["Remove Drink Selection"] = "order_remove_drink"
        self.order_menu_options["Suggest A Drink"] = "order_random_suggestion"
        self.order_menu_options["Confirm Order"] = "order_confirm"


    def _populate_random_drink_suggestions(self):
        self.random_drink_messages.append("Stay hydrated, drink water!")
        self.random_drink_messages.append("Have you ever tried @?")
        self.random_drink_messages.append("Enjoy a delicious #!")
        self.random_drink_messages.append("How about ordering @?")
        self.random_drink_messages.append("Feeling thirsty? Try @.")
        self.random_drink_messages.append("How does a lovely # sound?")