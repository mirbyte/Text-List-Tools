import os
import sys
import time
from colorama import Fore, Style
import shutil

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
		
        

     Algorithmic .txt list generator & modifier
      
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
        "List Combiner",
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

    with open(new_filename, "w", encoding="utf-8") as file:
        file.writelines(password + "\n" for password in unique_passwords)

    duplicates_removed = original_count - len(unique_passwords)

    print(f"New file saved as {new_filename}")
    print(f"Found and removed {duplicates_removed} duplicates.")
    print("")
    input("Press Enter to close...")


############ COMBINER #############
def combine_lists():
    # Get .txt files in the current dir
    txt_files = [f for f in os.listdir() if f.endswith(".txt")]

    if not txt_files:
        print("No .txt files found in the current directory.")
        return

    selected_files = []
    while True:
        print("\nAvailable text files:")
        for i, filename in enumerate(txt_files, start=1):
            selected = "✓" if filename in selected_files else " "
            print(f" [{selected}] {i}  {filename}")
        
        if selected_files:
            break
            
        print("\nSelect files to combine (enter numbers separated by spaces)")
        print("Enter 'all' to select all files")
        choice = input("> ").lower()
        
        if choice == 'all':
            selected_files = txt_files.copy()
            break
        else:
            try:
                choices = [int(c) for c in choice.split()]
                for c in choices:
                    filename = txt_files[c - 1]
                    if filename not in selected_files:
                        selected_files.append(filename)
                break
            except (ValueError, IndexError):
                print("Invalid selection. Please enter valid numbers.")

    output_filename = input("\nEnter output filename (without extension): ") + ".txt"
    
    # Add file existence check
    if os.path.exists(output_filename):
        overwrite = input(f"File {output_filename} already exists. Overwrite? (y/n): ").lower()
        if overwrite != 'y':
            print("Operation cancelled.")
            return

    try:
        # Process files in chunks to handle very large files
        chunk_size = 100000  # Process 100k lines at a time
        unique_lines = set()
        total_lines_processed = 0
        
        print("\nProcessing files...")
        for filename in tqdm(selected_files, desc="Files"):
            with open(filename, "r", encoding="utf-8", errors="ignore") as infile:
                for line in infile:
                    stripped_line = line.strip()
                    # Skip empty lines
                    if stripped_line:
                        unique_lines.add(stripped_line)
                    
                    # Process in chunks to avoid memory issues
                    if len(unique_lines) >= chunk_size:
                        with open(output_filename, "a" if total_lines_processed > 0 else "w", encoding="utf-8") as outfile:
                            outfile.writelines(line + "\n" for line in unique_lines)
                        total_lines_processed += len(unique_lines)
                        unique_lines.clear()
        
        # Write any remaining lines
        if unique_lines:
            with open(output_filename, "a" if total_lines_processed > 0 else "w", encoding="utf-8") as outfile:
                outfile.writelines(line + "\n" for line in unique_lines)
            total_lines_processed += len(unique_lines)
        
        print(f"\nSuccessfully combined {len(selected_files)} files into {output_filename}")
        print(f"Duplicates were automatically removed.")
    except Exception as e:
        print(f"\nError occurred while combining files: {e}")
    
    input("\nPress Enter to exit...")
    sys.exit()


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

    elif inp2 == 2: # Duplicate Remover
        clear()
        banner()
        remove_duplicates()
        
    elif inp2 == 3:  # List Combiner
        clear()
        banner()
        combine_lists()

    input("Press Enter to exit...")
    exit()
    
elif inp == 0:
    input("Press Enter to exit...")
    exit()

