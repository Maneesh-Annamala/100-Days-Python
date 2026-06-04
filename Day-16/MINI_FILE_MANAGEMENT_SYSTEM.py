# MINI FILE MANAGER
import os


def create_folder(folder_name):
    """
    Creates a new folder.
    """
    try:
        os.mkdir(folder_name)
        return f"The '{folder_name}' folder was created successfully."

    except FileExistsError:
        return "That folder already exists!"


def delete_folder(folder_name):
    """
    Deletes an empty folder.
    """
    try:
        os.rmdir(folder_name)
        return f"The '{folder_name}' folder was deleted successfully."

    except FileNotFoundError:
        return "Folder does not exist!"

    except OSError:
        return "Folder is not empty!"


def show_files(folder_path):
    """
    Shows all files and folders inside a given path.
    """
    try:
        return os.listdir(folder_path)

    except FileNotFoundError:
        return "That path does not exist!"


def create_file(file_name):
    """
    Creates a new file.
    """
    try:
        with open(file_name, "x"):
            pass

        return "File created successfully!"

    except FileExistsError:
        return "That file already exists!"


def delete_file(file_name):
    """
    Deletes a file.
    """
    try:
        os.remove(file_name)
        return "File deleted successfully!"

    except FileNotFoundError:
        return "That file does not exist!"


def rename_file(old_name, new_name):
    """
    Renames a file.
    """
    try:
        os.rename(old_name, new_name)
        return "File renamed successfully!"

    except FileNotFoundError:
        return "That file does not exist!"


while True:

    # Display menu
    try:
        choice = int(
            input(
                "\n1. Create Folder"
                "\n2. Delete Folder"
                "\n3. Show Files"
                "\n4. Create File"
                "\n5. Delete File"
                "\n6. Rename File"
                "\n7. Exit"
                "\n\nChoose what you want to do: "
            )
        )

    except ValueError:
        print("Please enter numbers only!")
        continue

    # Create Folder
    if choice == 1:
        folder_name = input("Enter folder name: ")
        print(create_folder(folder_name))

    # Delete Folder
    elif choice == 2:
        folder_name = input("Enter folder name to delete: ")
        print(delete_folder(folder_name))

    # Show Files
    elif choice == 3:
        folder_path = input("Enter folder path: ")
        result = show_files(folder_path)

        if isinstance(result, list):
            print("\nContents:")

            for item in result:
                print(item)

        else:
            print(result)

    # Create File
    elif choice == 4:
        file_name = input("Enter file name: ")
        print(create_file(file_name))

    # Delete File
    elif choice == 5:
        file_name = input("Enter file name to delete: ")
        print(delete_file(file_name))

    # Rename File
    elif choice == 6:
        old_name = input("Enter current file name: ")
        new_name = input("Enter new file name: ")
        print(rename_file(old_name, new_name))

    # Exit Program
    elif choice == 7:
        print("Exiting...")
        break

    # Invalid Choice
    else:
        print("Please choose a valid option!")