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
        else:
            print(f'"{user_choice}" is not a valid option.')


def view_contacts(contact_data):
    """View Contacts"""
    contacts = contact_data.get_all_records()
    for contact in contacts:       
        for contact_details in contact:
            print(f'{contact_details}: {contact[contact_details]}')
        print('----------\n')
    input("Press enter to return to main menu")


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
            confirm = input("\n(Press enter to continue / Enter Q to quit)\n")
            while confirm.capitalize() != "Q":
                cell = contact_data.find(contact_id)
                print("Please provide a new..")
                updated_contact = create_details_list()
                confirm = input("\n(Press enter to confirm changes / Q to quit)\n")
                contact_data.update(
                    f'B{cell.row}:F{cell.row}',
                    [updated_contact])
                print('\n----Contact updated successfully!----')
                break
            return False
        elif contact_id.capitalize() == "Q":
            print('---Quittinng and returning to main menu...---')
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
    contact_id = input("\nEnter an existing contact's ID (Q to quit)\n")
    if any(str(contact['Contact_Id']) == (contact_id) for contact in contacts):
        for contact in contacts:
            if contact['Contact_Id'] == int(contact_id):
                print("---Displaying Contact---\n")
                for key, value in contact.items():
                    print(f'{key}: {value}')
        return contact_id
    else:
        print("The user you're looking for doesn't seem to exist")
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
        fname = input("\nFirst name: ")
        lname = input("Last name: ")
        age = input("Age: ")
        while True:
            email = input("Email Address: ")
            if validate_email():
                break
            else:
                continue
            
        if:
            phone_number = input("Phone number: ")
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

start()
