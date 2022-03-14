class Person:
    """Person Object"""
    def __init__(self, contact_id, fname, lname, age, email, phone_number):
        """Instance of Person"""
        self.contact_id = contact_id
        self.fname = fname
        self.lname = lname
        self.age = age
        self.email = email
        self.phone_number = phone_number

    def __str__(self):
        return(
            f'Name: {self.fname} {self.lname}\n'
            f'Age: {self.age}\n'
            f'Email: {self.email}\n'
            f'Phone: {self.phone_number}\n'
            f'Id: {self.contact_id}'
        )
    

print("Welcome to the Contact Book!")
print("What would you like to do?\n")
print("1. View Contact")
print("2. Add Contact")
print("3. Edit Contact")
print("4. Remove Contact")
print("5. Exit Contact Book\n")
