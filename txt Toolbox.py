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
def list_cleaner():
    # get .txt files in the current dir
    txt_files = [f for f in os.listdir() if f.endswith(".txt")]

    if not txt_files:
        print("No .txt files found in the current directory.")
        return

    while True:
        for i, filename in enumerate(txt_files, start=1):
            print(f" {i}  {filename}")
        print("")
        filename_choice = input("\nEnter the corresponding number of the file to process: ")
        try:
            filename = txt_files[int(filename_choice) - 1]
            break
        except (ValueError, IndexError):
            print("Invalid choice. Please enter a valid number from the list.")

    try:
        with open(filename, "r", encoding="utf-8", errors="ignore") as file:
            passwords = file.readlines()

        original_count = len(passwords)

        print(f"Processing {filename}...")
        cleaned_passwords = set()
        for password in passwords:
            try:
                # cleaning process
                cleaned_password = ''.join(char for char in password if not char.isdigit() and char != '.' and char != ' ')
                cleaned_passwords.add(cleaned_password.strip())
            except UnicodeDecodeError:
                print(f"Warning: Skipping line with encoding error.")

        new_filename = filename.replace(".txt", "_cleaned.txt")

    except (FileNotFoundError, UnicodeDecodeError) as e:
        print(f"Error: Encountered an issue while processing {filename}: {e}")
        return  # Exit the function early if an error occurs

    # write to a new file using UTF-8
    with open(new_filename, "w", encoding="utf-8") as file:
        file.writelines(password + "\n" for password in cleaned_passwords)

    changes_made = original_count - len(cleaned_passwords)

    print(f"New file saved as {new_filename}")
    print("")
    input("Press Enter to close...")



## end of def list cleaner

############
def remove_duplicates():

    txt_files = [f for f in os.listdir() if f.endswith(".txt")]

    if not txt_files:
        print("No .txt files found in the current directory.")
        return

    while True:
        print("Text files found in the current directory:")
        for i, filename in enumerate(txt_files, start=1):
            print(f" {i}  {filename}")
        print("")
        filename_choice = input("\nEnter the corresponding number of the file to process: ")
        try:
            filename = txt_files[int(filename_choice) - 1]
            break
        except (ValueError, IndexError):
            print("Invalid choice. Please enter a valid number from the list.")

    try:
        with open(filename, "r", encoding="utf-8", errors="ignore") as file:
            passwords = file.readlines()

        original_count = len(passwords)

        print(f"Processing {filename}...")
        unique_passwords = set()
        for password in passwords:
            try:
                unique_passwords.add(password.strip())
            except UnicodeDecodeError:
                print(f"Warning: Skipping line with encoding error.")

        new_filename = filename.replace(".txt", "_uniques.txt")

    except (FileNotFoundError, UnicodeDecodeError) as e:
        print(f"Error: Encountered an issue while processing {filename}: {e}")
        return


    with open(new_filename, "w", encoding="utf-8") as file:  # specify UTF-8 encoding
        file.writelines(password + "\n" for password in unique_passwords)

    duplicates_removed = original_count - len(unique_passwords)

    print(f"New file saved as {new_filename}")
    print(f"Found and removed {duplicates_removed} duplicates.")
    print("")
    input("Press Enter to close...")

## end of def duplicate remover

############

banner()
menu()

print(" Select Option: ")
inp = int(input(" > "))



#############GENERATOR##
if inp == 1:
    clear()
    banner()

    def get_char_set():
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
        banner()
        list_cleaner()

    
    if inp2 == 2: # Duplicate Remover
        clear()
        banner()
        remove_duplicates()
        
    

    
    input("Press Enter to exit...")
    exit()
    
    
    
    




elif inp == 0:
    input("Press Enter to exit...")
    exit()
