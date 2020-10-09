from random import randrange

def intro(user):
    ascii_title = """:::::::::::   ::::::::    ::::    :::   :::    ::::::::  
    :+:      :+:    :+:   :+:+:   :+:   :+:   :+:    :+: 
    +:+      +:+    +:+   :+:+:+  +:+   +:+   +:+        
    +#+      +#+    +:+   +#+ +:+ +#+   +#+   +#+        
    +#+      +#+    +#+   +#+  +#+#+#   +#+   +#+        
    #+#      #+#    #+#   #+#   #+#+#   #+#   #+#    #+# 
    ###       ########    ###    ####   ###    ########"""

    welcome_message = f"Welcome to Tonic {user}!"

    rand_int = randrange(0, 5)

    if rand_int == 0:
        ascii_title = ascii_title.replace('#', 'O').replace('+', 'o')
    elif rand_int == 1:
        ascii_title = ascii_title.replace('#', '|').replace('+', '!')
    elif rand_int == 2:
        ascii_title = ascii_title.replace('#', '^').replace('+', 'X').replace(':', 'v')
    elif rand_int == 3:
        ascii_title = """*********     ********    ****    ***   ***    ******** 
    ***      ***    ***   *****   ***   ***   ***     ** 
    ***      ***    ***   ******  ***   ***   ***      
    /\/      \/\    /\/   /\/ /\/ /\/   \/\   /\/       
    ###      ###    ###   ###  ######   ###   ###        
    ###      ###    ###   ###   #####   ###   ###    ### 
    ###       ########    ###    ####   ###    ########"""

    return f"\n{ascii_title}\n \n{welcome_message}"