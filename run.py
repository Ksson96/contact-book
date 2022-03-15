class Person:
    """Person Object"""
    __CONTACT_ID = 1

    def __init__(self, fname, lname, age, email, phone_number):
        """Instance of Person"""
        self.fname = fname
        self.lname = lname
        self.age = age
        self.email = email
        self.phone_number = phone_number
        self.contact_id = Person.__CONTACT_ID
        Person.__CONTACT_ID += 1

    def __str__(self):
        return(
            f'Id: {self.contact_id}\n'
            f'Name: {self.fname} {self.lname}\n'
            f'Age: {self.age}\n'
            f'Email: {self.email}\n'
            f'Phone: {self.phone_number}\n'
        )


contacts = list()


def view_contacts():
    """View Contacts"""
    for contact in contacts:
        print(contact)


def create_contact():
    """Create Contact"""
    fname = input("First name: ")
    lname = input("Last name: ")
    age = input("Age: ")
    email = input("Email Address: ")
    phone_number = input("Phone number: ")
    new_contact = Person(fname, lname, age, email, phone_number)
    contacts.append(new_contact)


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
        user_choice = input("Enter a number between 1-5: ")

        if user_choice == "1":
            view_contacts()

        elif user_choice == "2":
            create_contact()

        elif user_choice == "3":
            edit_contact()

        elif user_choice == "4":
            delete_contact()


def edit_contact():
    """Edit Contact"""
    edit_id = input("Please enter the ID of the contact you'd like to edit\n")
    for contact in contacts:
        if int(edit_id) == contact.contact_id:
            print(f'Current First Name: {contact.fname}\n')
            contact.fname = input("Enter new name: ")

            print(f'Current Last Name: {contact.lname}\n')
            contact.lname = input("Enter new name: ")

            print(f'Current Age: {contact.age}\n')
            contact.age = input("Enter new age: ")

            print(f'Current Email: {contact.email}\n')
            contact.email = input("Enter new email: ")

            print(f'Current Phone Number: {contact.phone_number}\n')
            contact.phone_number = input("Enter new phone number: ")


def delete_contact():
    """
    Delete function
    """
    print("Placeholder functionality")


start()