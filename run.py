class Person:
    """Person Object"""
    __CONTACT_ID = 1
    def __init__(self, fname, lname, age, email, phone_number ,contact_id):
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
            f'Id: {self.contact_id}'
            f'Name: {self.fname} {self.lname}\n'
            f'Age: {self.age}\n'
            f'Email: {self.email}\n'
            f'Phone: {self.phone_number}\n'
        )
    

print("Welcome to the Contact Book!")
print("What would you like to do?\n")
print("1. View Contact")
print("2. Add Contact")
print("3. Edit Contact")
print("4. Remove Contact")
print("5. Exit Contact Book\n")
user_choice = input("Enter a number between 1-5: ")

    
if user_choice == "1":
    print("You chose 1")

elif user_choice == "2":
    contact_id = 
    fname = input("First name: ")
    lname = input("Last name: ")
    age = input("Age: ")
    email = input("Email Address: ")
    phone_number = input("Phone number: ")
    