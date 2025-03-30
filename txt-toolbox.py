import os
import sys
import time
from colorama import Fore, Style
import shutil
import psutil
import multiprocessing
from tqdm import tqdm
import itertools
import string
import numpy as np



# This script is still in development, use at your own risk
# contact details can be found at github.com/mirbyte



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
    print(ORANGE + r"""
 _        _      _              _ _               
| |_ _  _| |_   | |_ ___   ___ | | |__   _____  __
| __\ \/ / __|  | __/ _ \ / _ \| | '_ \ / _ \ \/ /   
| |_ >  <| |_   | |_|(_) | (_) | | |_) | (_) >  <    
\___|_/\_\\__|  \__|\___/ \___/|_|_.__/ \___/_/\_\  
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
    input("Press Enter to continue...")
    # back to the menu


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
    input("Press Enter to continue...")
    # back to the menu


############ COMBINER #############
def combine_lists():
    txt_files = [f for f in os.listdir() if f.endswith(".txt")]

    if not txt_files:
        print("No .txt files found in the current directory.")
        return

    selected_files = []
    while True:
        print("\nAvailable text files:")
        for i, filename in enumerate(tqdm(txt_files), start=1):
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
    
    if os.path.exists(output_filename):
        overwrite = input(f"File {output_filename} already exists. Overwrite? (y/n): ").lower()
        if overwrite != 'y':
            print("Operation cancelled.")
            return

    try:
        chunk_size = 100000  # Process 100k lines at a time
        unique_lines = set()
        total_lines_processed = 0
        total_lines_read = 0
        
        print("\nProcessing files...")
        for filename in tqdm(selected_files, desc="Files"):
            try:
                with open(filename, "r", encoding="utf-8", errors="ignore") as infile:
                    for line in infile:
                        total_lines_read += 1
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
            except Exception as e:
                print(f"\nWarning: Error processing file {filename}: {e}")
                print("Continuing with other files...")
                continue
        
        # Write any remaining lines
        if unique_lines:
            with open(output_filename, "a" if total_lines_processed > 0 else "w", encoding="utf-8") as outfile:
                outfile.writelines(line + "\n" for line in unique_lines)
            total_lines_processed += len(unique_lines)
        
        print(f"\nSuccessfully combined {len(selected_files)} files into {output_filename}")
        unique_count = total_lines_processed
        print(f"Read {total_lines_read:,} lines, wrote {unique_count:,} unique lines") 
        print(f"Removed {total_lines_read - unique_count:,} duplicates")
    except Exception as e:
        print(f"\nError occurred while combining files: {e}")
        return

    input("\nPress Enter to continue...")
    return # sys exit


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
            print(" [1] numbers only")
            print(" [2] lowercase only")
            print(" [3] numbers + lowercase")
            print(" [4] numbers + all letters")
            print(" [5] numbers + all letters + special characters")
            print(" [6] custom character set")
            print("")
            choice = input("Choose the character set: ")
            if choice in ("1", "2", "3", "4", "5", "6"):
                if choice == "1":
                    return string.digits
                elif choice == "2":
                    return string.ascii_lowercase
                elif choice == "3":
                    return string.digits + string.ascii_lowercase
                elif choice == "4":
                    return string.digits + string.ascii_letters
                elif choice == "5":
                    return string.digits + string.ascii_letters + string.punctuation
                else:  # Choice 6
                    custom_chars = input("Enter your custom character set: ")
                    if not custom_chars:
                        print("Character set cannot be empty")
                        continue
                    if len(set(custom_chars)) < 3:
                        print("Warning: Very small character set")
                    return ''.join(sorted(set(custom_chars)))
            else:
                print("Invalid choice. Please enter 1, 2, 3, 4, 5, or 6.")

    chars = get_char_set()

    # In the generator section:
    length = 0
    while length <= 0:
        try:
            length = int(input("Length? "))
            if length <= 0:
                print("Length must be a positive number.")
        except ValueError:
            print("Please enter a valid number.")
    
    # warning for large combinations
    total_combinations = len(chars) ** length
    if total_combinations > 100000000:
        print(f"Warning: This will generate {total_combinations:,} combinations.")
        confirm = input("This may take a long time and use a lot of disk space. Continue? (y/n): ").lower()
        if confirm != 'y':
            print("Operation cancelled.")
            input("Press Enter to close...")
            exit()

    # Fix the numeric generation case by removing the incorrect return
    def get_safe_chunk_size(current_chunk_size, length, chars):
        """Dynamically adjust chunk size based on available RAM"""
        mem = psutil.virtual_memory()
        safe_threshold = 0.7  # Use max 70% of available RAM
        
        # Calculate memory needed for one chunk (approximate)
        bytes_per_item = length * 4  # Rough estimate (4 bytes per char)
        memory_needed = current_chunk_size * bytes_per_item
        
        # Reduce chunk size if needed
        while memory_needed > (mem.available * safe_threshold):
            current_chunk_size = current_chunk_size // 2
            memory_needed = current_chunk_size * bytes_per_item
            if current_chunk_size < 1000:  # Minimum chunk size
                raise MemoryError("Not enough memory to proceed safely")
        
        return current_chunk_size

    # Handle different character set options
    if chars == string.digits:
        chunk_size = get_safe_chunk_size(1_000_000, length, chars)
        filename_prefix = "numbers_only"
        output_filename = f"{filename_prefix}_len{length}.txt"
        
        if os.path.exists(output_filename):
            overwrite = input(f"File {output_filename} already exists. Overwrite? (y/n): ").lower()
            if overwrite != 'y':
                print("Operation cancelled.")
                input("Press Enter to close...")
                exit()

        # Generate all possible number combinations
        with open(output_filename, "wb") as file:
            total_numbers = 10**length
            chunk_size = min(chunk_size, total_numbers)
            
            for start in tqdm(range(0, total_numbers, chunk_size), 
                            desc="Generating", 
                            unit="chunk"):
                end = min(start + chunk_size, total_numbers)
                chunk = [f"{num:0{length}d}\n" for num in range(start, end)]
                file.write(b''.join(s.encode('utf-8') for s in chunk))
        
        print(f"Saved to {output_filename}")
        input("Press Enter to close...")
        exit()
    
    else: # For mixed character sets (options 2-6)
        try:
            # filename prefix
            if chars == string.ascii_lowercase:
                filename_prefix = "lowercase_only"
            elif chars == string.digits + string.ascii_lowercase:
                filename_prefix = "numbers_lowercase"
            elif chars == string.digits + string.ascii_letters:
                filename_prefix = "numbers_allletters"
            elif chars == string.digits + string.ascii_letters + string.punctuation:
                filename_prefix = "all_chars"
            else:
                filename_prefix = "custom_chars"
            
            output_filename = f"{filename_prefix}_len{length}.txt"
            
            if os.path.exists(output_filename):
                overwrite = input(f"File {output_filename} already exists. Overwrite? (y/n): ").lower()
                if overwrite != 'y':
                    print("Operation cancelled.")
                    input("Press Enter to close...")
                    exit()

            chunk_size = get_safe_chunk_size(100_000, length, chars)
            
            # Generate combinations using a more reliable approach
            with open(output_filename, "wb") as file:
                char_list = list(chars)
                total_combinations = len(chars) ** length
                
                if total_combinations == 0:
                    raise ValueError("No combinations possible with current character set")
                
                pbar = tqdm(total=total_combinations, desc="Generating")
                
                # Use a simpler chunking approach
                product_iter = itertools.product(char_list, repeat=length)
                while True:
                    chunk = []
                    # Get next chunk_size items
                    for _ in range(chunk_size):
                        try:
                            combo = next(product_iter)
                            chunk.append(''.join(combo) + '\n')
                        except StopIteration:
                            break
                    
                    if not chunk: # No more combinations
                        break
                        
                    file.write(b''.join(s.encode('utf-8') for s in chunk))
                    pbar.update(len(chunk))
                    file.flush() # Ensure data is written to disk
                
                pbar.close()
            
            print(f"Saved to {output_filename}")
            input("Press Enter to close...")
            exit()
            
        except Exception as e:
            print(f"Error during generation: {str(e)}")
            input("Press Enter to close...")
            exit()


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
        
    elif inp2 == 3: # List Combiner
        clear()
        banner()
        combine_lists()
    
    elif inp2 == 0: # Exit
        print("Exiting...")
        exit()
    
    else: # Invalid option
        print("Invalid option selected.")
        input("Press Enter to return to main menu...")



    clear()
    banner()
    menu()
    print(" Select Option: ")
    inp = int(input(" > "))
    # This will loop back to the main menu processing




if __name__ == "__main__":
    main()
  
