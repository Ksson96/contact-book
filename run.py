import gspread
from google.oauth2.service_account import Credentials
import re


SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('contact_book')


def start():
    """
    Displays all menu options to the user
    """
    user_choice = ""
    while user_choice != "5":
        print('''
    ------------------------------------
    --- Welcome to the Contact Book! ---
    ------------------------------------
    ''')
        print('''
    ---------------------------
    ---------Main Menu---------
    ---------------------------
    What would you like to do?
    ----------------
    1. View Contacts
    2. Add Contact
    3. Edit Contact
    4. Remove Contact
    5. Exit Contact Book
    ----------------
        ''')
        user_choice = input("\nEnter a number between 1-5: \n")
        contact_data = SHEET.worksheet('contact_data')
        if user_choice == "1":
            print('\n--- Displaying All Contacts ---\n')
            view_contacts(contact_data)
        elif user_choice == "2":
            new_contact_id = calc_new_contact_id(contact_data)
            create_contact(contact_data, new_contact_id)
        elif user_choice == "3":
            edit_contact(contact_data)
        elif user_choice == "4":
            delete_contact(contact_data)
        elif user_choice == "5":
            print("Exiting Contact Book")
        else:
            print(f'"{user_choice}" is not a valid option.')


def view_contacts(contact_data):
    """View Contacts"""
    contacts = contact_data.get_all_records()
    for contact in contacts:       
        for contact_details in contact:
            print(f'{contact_details}: {contact[contact_details]}')
        print('----------\n')
    print("Showing all existing contacts")


def create_contact(contact_data, contact_id):
    """Create Contact"""
    print("Creating a new contact...")
    new_contact = create_details_list()
    new_contact.insert(0, contact_id)
    contact_data.append_row(new_contact)
    print("New contact created successfully")


def edit_contact(contact_data):
    """Edit Contact"""
    while True:
        contact_id = display_contact(contact_data)
        if contact_id:
            while True:
                confirm = input("\n(Press enter to continue / Enter Q to quit)\n")
                if confirm.capitalize() == "Q":
                    print("\nQuitting and returning to main menu...\n")
                    return False
                else:
                    cell = contact_data.find(contact_id)
                    print("Editing contact..")
                    updated_contact = create_details_list()
                    confirm = input("\n(Press enter to confirm changes / Q to quit)\n")
                if confirm.capitalize() == "Q":
                    print("Quitting and returning to main menu...")
                    return False
                else:
                    contact_data.update(
                        f'B{cell.row}:F{cell.row}',
                        [updated_contact])
                    print('\n----Contact updated successfully!----')
                    return False
        else:
            view_contacts(contact_data)
            input("\nPress Enter to continue")
            continue

        break
    else:
        print('---Quitting and returning to main menu...---')
        return False


def delete_contact(contact_data):
    """ Delete Contact """
    while True:
        contact_id = display_contact(contact_data)
        if contact_id:
            confirm = input("\nAre you sure you wish to permanently delete this contact? Y: Yes / N: No\n")
            if confirm.capitalize() == "Y":
                contact_data.delete_rows(contact_data.find(contact_id).row)
                print("The requested contact has been permanently deleted!\n")
                print("Returning to main menu...\n")
                break
            elif confirm.capitalize() == "N":
                print("\nReturning to main menu...")
                break
            else:
                print("Please only enter Y / N")


def display_contact(contact_data):
    """
    Returns contact information for given contact id
    """
    contacts = contact_data.get_all_records()
    contact_id = input("\nEnter an existing contact's ID:\n")
    if any(str(contact['Contact_Id']) == (contact_id) for contact in contacts):
        for contact in contacts:
            if contact['Contact_Id'] == int(contact_id):
                print("---Displaying Contact---\n")
                for key, value in contact.items():
                    print(f'{key}: {value}')
        return contact_id
    else:
        print("The user you're looking for doesn't seem to exist\n")
        return False


def calc_new_contact_id(contact_data):
    """
    Convert str list of IDs to int and return biggest number +1
    """
    contact_ids = contact_data.col_values(1)
    del contact_ids[0]

    return max([int(x) for x in contact_ids]) + 1


def create_details_list():
    """
    Returns contact details from user input as a list
    """
    while True:
        fname = input("\nFirst name: ")
        if not fname.isalpha():
            print("Please only enter letters between a-Z")
            continue
        else:
            break
    while True:
        lname = input("\nLast name: ")
        if not lname.isalpha():
            print("Please only enter letters between a-Z")
            continue
        else:
            break
    while True:
        age = input("\nAge: ")
        if not validate_age(age):
            continue
        else:
            break
    while True:
        email = input("\nEmail Address: ")
        if not validate_email(email):
            continue
        else:
            break
    while True:
        phone_number = input("\nPhone number: ")
        if not validate_phone(phone_number):
            continue
        else:
            break

    return [fname, lname, age, email, phone_number]


def validate_email(email):
    """
    Validates user inputted email adress
    """
    rex = "^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$"

    if(re.fullmatch(rex, email)):
        return True
    else:
        print("Email-adress not valid!")
        return False


def validate_phone(phone):
    """
    Validates user inputted phone number
    """
    rex = r"^[0-9]"
    
    if (re.match(rex, phone)) and len(phone) < 11:
        return True
    else:
        print("Please enter a valid number")


def validate_age(age):
    """
    Validates user inputted age
    """
    rex = "^[1-9][0-9]?$|^100$"
    if(re.fullmatch(rex, age)):
        return True
    else:
        print("Please enter a valid age")
        return False


start()
