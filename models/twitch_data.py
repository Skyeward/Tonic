import socket
import time
from tools.tonic_format import format_string as fmat

class TwitchData():
    def __init__(self):
        self.server = "irc.twitch.tv"
        self.port = 6667
        self.auth = "oauth:wwsov1kd1dc9926vmxxv0qgm9pp8bn"
        self.bot = "TonicBot"
        self.channel = "tonicapp"
        self.owner = "tonicapp"
        self.irc = None
        self.user = None

        self.generate_socket()
        self.join_chat()
        

    def generate_socket(self):
        self.irc = socket.socket()
        self.irc.connect((self.server, self.port))
        self.irc.send(("PASS " + self.auth + "\n" +
                        "NICK " + self.bot + "\n" + 
                        "JOIN #" + self.channel + "\n").encode())


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
            return None


    def find_command(self, message_type, **kwargs):
        while True:
            try:
                readbuffer = self.irc.recv(1024).decode()
            except:
                readbuffer = ""
            
            for line in readbuffer.split("\r\n"):
                if line != "":
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
