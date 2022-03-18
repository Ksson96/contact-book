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


def view_contacts(contact_data):
    """View Contacts"""
    print('****--- Displaying All Contacts ---***\n')
    contacts = contact_data.get_all_records()
    for contact in contacts:       
        for contact_details in contact:
            print(f'{contact_details}: {contact[contact_details]}')
        print('----------\n')


def calc_new_contact_id(contact_data):
    """
    Convert str list of IDs to int and return biggest number +1
    """
    contact_ids = contact_data.col_values(1)
    del contact_ids[0]

    return max([int(x) for x in contact_ids]) + 1


def create_contact(contact_data, new_contact_id):
    """Create Contact"""

    contact_id = new_contact_id
    fname = input("First name: ")
    lname = input("Last name: ")
    age = input("Age: ")
    email = input("Email Address: ")
    phone_number = input("Phone number: ")
    new_contact = [contact_id, fname, lname, age, email, phone_number]
    contact_data.append_row(new_contact)


def start():
    """
    Displays all menu options to the user
    """
    user_choice = ""
    print("Welcome to the Contact Book!")
    while user_choice != "5":

        print("What would you like to do?\n")
        print("1. View Contacts")
        print("2. Add Contact")
        print("3. Edit Contact")
        print("4. Remove Contact")
        print("5. Exit Contact Book\n")
        user_choice = input("Enter a number between 1-5: \n")

        contact_data = SHEET.worksheet('contact_data')
    
        if user_choice == "1":
            view_contacts(contact_data)

        elif user_choice == "2":
            new_contact_id = calc_new_contact_id(contact_data)
            create_contact(contact_data, new_contact_id)

        elif user_choice == "3":
            edit_contact(contact_data)

        elif user_choice == "4":
            delete_contact(contact_data)


# def find_contact(contact_data, contact_id):
#     cell = contact_data.find(contact_id)
#     return cell


def edit_contact(contact_data):
    """Edit Contact"""
    contact_id = input("Please enter the ID of the contact you'd like to edit\n")
    contacts = contact_data.get_all_records()
    cell = contact_data.find(contact_id)
    for contact in contacts:
        for contact_details in contact:
            if contact[contact_details] == int(contact_id):
                fname = input("Enter new name: ")                
                lname = input("Enter new name: ")                
                age = input("Enter new age: ")                
                email = input("Enter new email: ")                
                phone_number = input("Enter new phone number: ")
                contact_data.update(f'B{cell.row}:F{cell.row}', [[fname, lname, age, email, phone_number]])
    print('Contact updated successfully!')


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
    for contact in contacts:
        if contact['Contact_Id'] == int(contact_id):
            for key, value in contact.items():
                print(f'{key}: {value}')
# cell = contact_data.find(contact_id)
# contact = contact_data.row_values(cell.row)
# print(f'Id: {contact[0]} \n')
# print(f'Name: {contact[1]} {contact[2]} \n')
# print(f'Age: {contact[3]}\n')
# print(f'Email: {contact[4]}\n')
# print(f'Number: {contact[5]}\n')


start()
