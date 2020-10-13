import socket
import time
from tools.tonic_format import format_string as fmat
from random import randrange as randrange

class TwitchData():
    def __init__(self, wordlist, possible_passwords):
        self.server = "irc.twitch.tv"
        self.port = 6667
        self.auth = "oauth:wwsov1kd1dc9926vmxxv0qgm9pp8bn"
        self.bot = "TonicBot"
        self.channel = "tonicapp"
        self.owner = "tonicapp"
        self.irc = None
        self.user = None
        self.possible_passwords = possible_passwords
        self.wordlist = wordlist
        self.pw_progress = "_____"

        self.generate_socket()
        self.join_chat()
        

    def generate_socket(self):
        self.irc = socket.socket()
        self.irc.connect((self.server, self.port))
        self.irc.send(("PASS " + self.auth + "\n" +
                        "NICK " + self.bot + "\n" + 
                        "JOIN #" + self.channel + "\n").encode())


    def get_word(self):
        return self.possible_passwords[randrange(0, len(self.possible_passwords) - 1)]


    def join_chat(self):
        loading = True

        while loading == True:
            readbuffer_join = self.irc.recv(1024)
            readbuffer_join = readbuffer_join.decode()

            for line in readbuffer_join.split("\n"):
                loading = self.loading_complete(line)
                
                if loading == False:
                    break


    def loading_complete(self, line):
        if ("End of /NAMES list" in line):
            return False
        else:
            return True


    def get_user(self, line):
        if ".tmi.twitch.tv PRIVMSG" in line:
            return line.split("!")[0][1:]
        else:
            return None


    def get_message(self, line):
        if ".tmi.twitch.tv PRIVMSG" in line:
            splits = line.split("p :")
            splits_without_lead = "".join(splits[1:])
            return splits_without_lead
        else:
            return ""


    def find_command(self, message_type, **kwargs):
        order_dict = {}
        random_fails = ["Unlucky!", "Try again!", "That's not it!", "Nope, sorry!", "Good try, but no!", "Ouch!"]

        if message_type == "order":
            for customer in kwargs["order"].customers:
                order_dict[customer.name.lower()] = customer.favourite_drink
        
        while True:
            try:
                readbuffer = self.irc.recv(1024).decode()
            except:
                readbuffer = ""
            
            for line in readbuffer.split("\r\n"):
                if line != "" and line != None:
                    if message_type == "find user":
                        if self.get_message(line).lower().replace('"', "'").replace("'", '"').replace("!", "").replace(".", "").replace(" ", "") == "me":
                            self.user = self.get_user(line)

                            time.sleep(0.1)
                            return self.user
                    elif message_type == "index":
                        if self.get_user(line) == self.user:
                            message = self.get_message(line)

                            try:
                                index = int(message)

                                if (0 <= index < kwargs["number_of_options"]):
                                    
                                    time.sleep(0.1)
                                    return index
                            except:
                                pass
                    elif message_type == "search":
                        if self.get_user(line) == self.user:
                            
                            time.sleep(0.1)
                            return fmat(self.get_message(line)).lower()
                    elif message_type == "unique string":
                        if self.get_user(line) == self.user:
                            message = fmat(self.get_message(line)).lower()

                            if message in kwargs["unavailable_strings"]:
                                print("That already exists. Try a different name!")
                            else:
                                time.sleep(0.1)
                                return message
                    elif message_type == "order":
                        message = fmat(self.get_message(line).lower().replace('"', "'").replace("'", '"').replace("!", "").replace(".", ""))
                        order_user = self.get_user(line)

                        if (message == "done" or message == "stop") and (order_user == self.user):
                            return order_dict
                        elif message[:6] == "order " and len(message) > 6:
                            if len(message) > 30:
                                print(f"sorry {order_user}, that drink name is too long! Drink names should be no more than 30 characters.")
                                print()
                            else:
                                message = message[6:]
                                
                                if order_user in order_dict.keys():
                                    print(f"{order_user}, you've changed your drink order to '{message}'!")
                                    print()
                                else:
                                    print(f"{order_user}, your order of '{message}' has been added!")
                                    print()
                                
                                order_dict[order_user] = message
                    elif message_type == "game":
                        message = fmat(self.get_message(line).lower())
                        guesser = self.get_user(line)
                        pw = kwargs["pw"]
                        
                        if self.user != guesser and len(message) == 5:
                            if message in self.wordlist:
                                valid_word = True

                                for i in range(len(message)):
                                    if self.pw_progress[i] != "_" and message[i] != pw[i]:
                                        valid_word = False

                                if valid_word == False:
                                    print(f"Sorry {guesser.upper()}, '{message}' doesn't fit the puzzle so far. Take a look below.")
                                    print()
                                    print(self.pw_progress[0].upper() + " " + self.pw_progress[1].upper() + " " + self.pw_progress[2].upper() + " " + self.pw_progress[3].upper() + " " + self.pw_progress[4].upper())
                                    print()
                                else:
                                    letters_to_add = []

                                    for i in range(len(pw)):
                                        if self.pw_progress[i] == "_" and pw[i] == message[i]:
                                            letters_to_add.append(i)

                                    for i in letters_to_add:
                                        if i == 5:
                                            self.pw_progress = self.pw_progress[:i] + pw[i]
                                        if i == 0:
                                            self.pw_progress = pw[i] + self.pw_progress[i + 1:]
                                        else:
                                            self.pw_progress = self.pw_progress[:i] + pw[i] + self.pw_progress[i + 1:]

                                    if pw == self.pw_progress:
                                        print(f"{guesser.upper()} correctly guessed the password {pw.upper()}. Congratulations! You can now control the app.")
                                        self.user = guesser
                                        time.sleep(1.5)
                                        return
                                    elif len(letters_to_add) == 0:
                                        print(f"{guesser.upper()}, you didn't find any new letters. " + random_fails[randrange(0, len(random_fails) - 1)])
                                    elif len(letters_to_add) == 1:
                                        print(f"{guesser.upper()}, you found 1 new letter, well done!")
                                    else:
                                        print(f"{guesser.upper()}, you found {len(letters_to_add)} new letters, well done!")

                                    print()
                                    print(self.pw_progress[0].upper() + " " + self.pw_progress[1].upper() + " " + self.pw_progress[2].upper() + " " + self.pw_progress[3].upper() + " " + self.pw_progress[4].upper())
                                    print()
                            else:
                                print(f"Sorry {guesser.upper()}, '{message}' is not a recognised word.")
                                print()
                                print(self.pw_progress[0].upper() + " " + self.pw_progress[1].upper() + " " + self.pw_progress[2].upper() + " " + self.pw_progress[3].upper() + " " + self.pw_progress[4].upper())
                                print()
                        elif self.user == guesser and message == "cancel":
                            print(f"Game over! The word was {pw.upper()}. The app user is still {self.user}.")
                            time.sleep(1.5)
                            return


