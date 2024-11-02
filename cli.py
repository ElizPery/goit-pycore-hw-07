from collections import UserDict
from datetime import datetime
from re import match

# Common class for fields
class Field:
    def __init__(self, value: str) -> None:
        self.value = value

    def __str__(self) -> str:
        return str(self.value)

# Class for name
class Name(Field):
		pass

# Class for phone with validation (10 numbers)
class Phone(Field):
    def __init__(self, phone: str):
        # Validation of name
        if len(phone) == 10 and all([el.isdigit() for el in phone]):
            super().__init__(phone)
        else:
            raise ValueError('Invalid date format. Phone must contain 10 numbers')

# Class for birthday with validation (format 'DD.MM.YYYY')
class Birthday(Field):
    def __init__(self, date: str):
        try:
            value = datetime.strptime(date, '%d.%m.%Y').date()
            super().__init__(value)
        except ValueError:
            raise ValueError('Invalid date format. Use DD.MM.YYYY')
    
    def __str__(self):
        return datetime.strftime(self.value, '%d.%m.%Y')

# Class for record whoch contain name and list of Phones
class Record:
    def __init__(self, name: str) -> None:
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    # Add phone to the record by taking phone, if phone is already exist return
    def add_phone(self, phone: str):
        if str(Phone(phone)) in self.phones:
            return 'Phone is already exist'
        self.phones.append(str(Phone(phone)))
        return self.phones
    
    # # Remove phone from the record by taking phone, if phone not exist return
    # def remove_phone(self, phone: str):
    #     if str(Phone(phone)) not in self.phones:
    #         return 'Phone is not in phones'
    #     self.phones = [el for el in self.phones if not el == str(Phone(phone))]
    #     return self.phones
    
    # # Edit phone from the record by taking phone and new phone, if phone not exist return
    # def edit_phone(self, phone: str, new_phone: str):
    #     if str(Phone(phone)) in self.phones:
    #         phone_index = self.phones.index(phone)
    #         self.phones.remove(phone)
    #         self.phones.insert(phone_index, new_phone)
    #         return self.phones
    #     else:
    #         return 'Phone is not in phones'

    # # Find phone from the record by taking phone, if phone not exist return
    # def find_phone(self, phone: str):
    #     if str(Phone(phone)) not in self.phones:
    #         return 'Phone is not in phones'
    #     return phone
    
    # # Add birthday to the record by taking birthday (format 'DD.MM.YYYY')
    # def add_birthday(self, date: str):
    #     self.birthday = str(Birthday(date))
    #     return self.birthday

    # def __str__(self):
    #     return f'Contact name: {self.name}, phones: {'; '.join(p for p in self.phones)}, birthday: {self.birthday if self.birthday else "unknown"}'

# Class for address book
class AddressBook(UserDict):

    # Add record to the dict by taking record
    def add_record(self, record: Record):
        self.data[str(record.name)] = {'phones': record.phones, 'birthday': record.birthday}

        return self.data

    # Find record in dict by taking name
    def find(self, name: str):
        if name in self.data:
            print(self.data[name])
            return self.data
        return None
    
    # # Delete record in dict by taking name, if name not exist return
    # def delete(self, name: str):
    #     if name in self.data:
    #         del self.data[name]
    #         return self.data
    #     return 'No records with this name'
    
    # # function that return list of users that have birthdays in upcoming week
    # def get_upcoming_birthdays(self):
    #     upcoming_birthdays = []

    #     for name, info in self.data.items():
    #         if not info['birthday']: continue
    #         print(info['birthday'])
    #         birthday_date = datetime.strptime(info['birthday'], '%d.%m.%Y').date()
    #         date_today = datetime.today().date()
    #         upcoming_birthday = datetime(year=date_today.year, month=birthday_date.month, day=birthday_date.day).date()

    #         # check if birthday already was this year, if yes, change date to the next year
    #         if(upcoming_birthday < date_today):
    #             upcoming_birthday = datetime(year=date_today.year + 1, month=birthday_date.month, day=birthday_date.day).date()

    #         # check if birthday in upcomming week
    #         if(upcoming_birthday.toordinal() - date_today.toordinal() <= 7):

    #             # check if birthday on weekend, if yes, change congratulation date to Monday
    #             if(upcoming_birthday.weekday() == 5):
    #                 upcoming_birthday = datetime(year=date_today.year, month=birthday_date.month, day=birthday_date.day + 2).date()
    #             if(upcoming_birthday.weekday() == 6):
    #                 upcoming_birthday = datetime(year=date_today.year, month=birthday_date.month, day=birthday_date.day + 1).date()

    #             upcoming_birthdays.append({'name': name, 'congratulation_date': datetime.strftime(upcoming_birthday, '%d.%m.%Y')})

    #     return upcoming_birthdays
    
# Decorator for handling errors of input
def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            if str(e) == 'Invalid date format. Phone must contain 10 numbers': return e
            return "Give me name and phone please."
        except IndexError:
            return "Enter user name"
        except KeyError:
            return "Contact is not in contacts"
    return inner

# Function take user input (first command) and return parsed data 
def parse_input(user_input: str):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

# Decorator to handle ValueError
@input_error
def add_contact(args: list[str], book: AddressBook) -> str:
    # Function add contact with data in args (name, phone) to the dict contacts

    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."

    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
        
    if phone:
        record.add_phone(phone)
    return message

# # Decorator to handle ValueError
# @input_error
# def change_contact(args: list[str], contacts: dict) -> str:
#     # Function takes data about contact and update phone of contact by name

#     name, phone = args

#     if name in contacts:
#         contacts[name] = phone
#         return 'Contact is updated!'
    
#     return 'Contact is not in contacts'

# # Decorator to handle IndexError and KeyError
# @input_error
# def show_phone(args: str, contacts: dict) -> str:
#     # Function takes name of contact and return its phone

#     name = args[0]

#     phone = contacts[name]
#     return phone
    
# # Function takes dict of contacts and return it, if no contacts return 'No contacts found'
# def show_all(contacts: dict) -> str:
#     all_contacts = []

#     if len(contacts) == 0:
#         return 'No contacts found'
#     for name, phone in contacts.items():
#         all_contacts.append(f'Contact: {name} {phone}\n')
    
#     return ''.join(all_contacts).strip()

# @input_error
# def add_birthday(args, book):
#     pass

# @input_error
# def show_birthday(args, book):
#     pass

# @input_error
# def birthdays(args, book):
#     pass


def main():
    book = AddressBook()

    print('Welcome to the assistance bot!')

    while True:
        user_input = input('Enter a command >>> ')
        command, *args = parse_input(user_input)

        if command in ['close', 'exit']:
            print('Goodbye!')
            break
        elif command == 'hello':
            print('Hello, how can I help you?')
        elif command == 'add':
            print(add_contact(args, book))
        # elif command == 'change':
        #     print(change_contact(args, contacts))
        # elif command == 'phone':
        #     print(show_phone(args, contacts))
        # elif command == 'all':
        #     print(show_all(contacts))
        else:
            print('Invalid command')

if __name__ == '__main__':
    main()
    

# book = AddressBook()
# john_record = Record("Bill")
# john_record.add_phone('0756489356')
# john_record.add_phone('0756489476')
# book.add_record(john_record)

# alex_record = Record("Alex")
# alex_record.add_phone('0756489355')
# alex_record.add_phone('0756489466')
# alex_record.add_birthday('10.10.2002')
# book.add_record(alex_record)
# print(alex_record)

# alina_record = Record("alina")
# alina_record.add_phone('0756489355')
# alina_record.add_phone('0756489466')
# alina_record.add_birthday('12.12.2002')
# book.add_record(alina_record)
# print(book.get_upcoming_birthdays())
