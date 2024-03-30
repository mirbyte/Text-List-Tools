import os
from tqdm import tqdm


def clean_passwords():
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


clean_passwords()
