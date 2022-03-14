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
print("Choose one of the following options by entering a number between 1-5:")


