import gspread
from google.oauth2.service_account import Credentials


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
    user_choice = ""
    while user_choice != "5":
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


def create_contact(contact_data, contact_id):
    """Create Contact"""

    new_contact = create_details_list()
    new_contact.insert(0, contact_id)
    contact_data.append_row(new_contact)


def edit_contact(contact_data):
    """Edit Contact"""
    while True:
        contact_id = input("Please enter the ID of the contact you'd like to edit\n")
        cell = contact_data.find(contact_id)
        display_contact(contact_data, contact_id)
        if cell:
            updated_contact = create_details_list()
            contact_data.update(
                f'B{cell.row}:F{cell.row}',
                [updated_contact])
            print('\n----Contact updated successfully!----')
            break
        else:
            continue


def delete_contact(contact_data):
    """ Delete Contact """

    contact_id = input("Please enter the ID of the contact you'd like to remove\n")
    print("---Displaying Contact to Remove---\n")
    display_contact(contact_data, contact_id)
    confirmation = input("\nAre you sure you wish to permanently remove this contact? Y: Yes / N: No\n").capitalize()
    if confirmation == "Y":
        contact_data.delete_rows(contact_data.find(contact_id).row)
    else:
        start()


def display_contact(contact_data, contact_id):
    """
    Returns contact information for given contact id
    """
    contacts = contact_data.get_all_records()
    if any(contact['Contact_Id'] == int(contact_id) for contact in contacts):
        for contact in contacts:
            if contact['Contact_Id'] == int(contact_id):
                print("---Displaying Contact---\n")
                for key, value in contact.items():
                    print(f'{key}: {value}')
    else:
        print("The user you're looking for doesn't seem to exist")


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
    email = input("Email Address: ")
    phone_number = input("Phone number: ")
    return [fname, lname, age, email, phone_number]


# def confirm_choice(user_input):
#     if user_input.capitalize() == "Y":
#         return: 


start()
