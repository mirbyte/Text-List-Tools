import os
import sys
import time
from colorama import Fore, Style

# list generator
from tqdm import tqdm
import itertools
import string



RED = Fore.RED
ORANGE = Fore.LIGHTRED_EX
BLUE = Fore.BLUE
GREEN = Fore.GREEN
YELLOW = Fore.YELLOW
WHITE = Fore.WHITE
CYAN = Fore.CYAN
PURPLE = Fore.MAGENTA
END = Style.RESET_ALL

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def banner():
    clear()
    print(ORANGE + """
 _        _      _              _ _               
| |_ _  _| |_   | |_ ___   ___ | | |__   _____  __
| __\ \/ / __|  | __/ _ \ / _ \| | '_ \ / _ \ \/ /   
| |_ >  <| |_   | |_|(_) | (_) | | |_) | (_) >  <    
\___|_/\_\\___|  \__|\___/ \___/|_|_.__/ \___/_/\_\  
                github.com/mirbyte
		
        
        Algorithmic list generator & modifier
      
""" + END)


############
def menu():
    menu_items = [
        "Generate new list",
        "Modify existing",
    ]
    for index, item in enumerate(menu_items, start=1):
        print(f" [{index}] {item}")
        
    print(" [0] Exit")


############
def menu2():
    menu2_items = [
        "List Cleaner",
        "List Duplicates Remover",
        "Option 3",
        "Option 4"
    ]
    for index, item in enumerate(menu2_items, start=1):
        print(f" [{index}] {item}")
    print(" [0] Exit")


############


banner()
menu()

print(" Select Option: ")
inp = int(input(" > "))



#############GENERATOR##
if inp == 1:
    #print(" Enter the interface: (wlan0 | wlan1)")
    #inp1 = int(input(" > "))
    #print("")
    clear()
    banner()

    def get_char_set():
        """
        Prompts the user to choose the character set and returns a string.
        """
        while True:
            print("  1  numbers only")
            print("  2  numbers + lowercase")
            print("  3  numbers + all letters")
            print("  4  numbers + all letters + special characters")
            print("")
            choice = input("Choose the character set: ")
            if choice in ("1", "2", "3", "4"):
                if choice == "1":
                    return string.digits
                elif choice == "2":
                    return string.digits + string.ascii_lowercase
                elif choice == "3":
                    return string.digits + string.ascii_letters
                else:  # Choice 4
                    return string.digits + string.ascii_letters + string.punctuation
            else:
                print("Invalid choice. Please enter 1, 2, 3, or 4.")

    chars = get_char_set()

    length = int(input("Length of combinations? "))
    total_combinations = len(chars) ** length

    with open("combinations.txt", "w") as file:
        for i, combo in tqdm(
            enumerate(itertools.product(chars, repeat=length)),
            total=total_combinations,
            desc="Progress"
        ):
            file.write("".join(combo) + "\n")

    print("saved to combinations.txt")

    input("Press Enter to close...")


########################

 
elif inp == 2:
    clear()
    banner()
    menu2()

    print(" Select Option: ")
    inp2 = int(input(" > "))
    
    if inp2 == 1: # List Cleaner
        clear()
        input("option 1 selected")

    
    if inp2 == 2: # Duplicate Remover
        clear()
        input("option 2 selected")
        
    

    
    input("Press Enter to exit...")
    exit()
    
    
    
    




elif inp == 0:
    input("Press Enter to exit...")
    exit()
