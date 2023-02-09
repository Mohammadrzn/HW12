from typing import Optional
from admin import *
import platform
import datetime
import pickle
import time
import uuid
import sys
import os

RED = "\033[0;31m"
GREEN = "\033[0;32m"
BLUE = "\033[0;34m"
YELLOW = "\033[1;33m"
END = "\033[0m"


logger_ticket = logging.getLogger('metro')
logger_bank = logging.getLogger('metro')
logger_trip = logging.getLogger('metro')


class Ticket:
    """Class for creating tickets and using them"""

    def __init__(self, ticket_type, amount=0, ticket_date=None):
        """
        :param ticket_type: single trip, credit & long term
        :param amount: the amount of credit and long term tickets
        :param ticket_date: The time when the ticket was purchased
        """
        self.ticket_type = ticket_type
        self.amount = amount
        self.ticket_serial = str(uuid.uuid4())
        self.validate = True
        self.ticket_date = ticket_date
        self.ticket_use_time = None
        self.trip = []
        logger_ticket.info(f'{datetime.date.today()}: Ticket class called ')

    def expire_ticket(self):
        if self.ticket_type == "3":
            self.ticket_date = datetime.date.today() + datetime.timedelta(days=365)

    def ticket_charge(self, amount):
        if self.ticket_type != "1":
            self.amount += amount
        return self.amount

    def validate_ticket(self):
        if self.ticket_type == "1":
            self.validate = False
        elif self.ticket_type == "2" and self.amount < 2500:
            self.validate = False
        elif self.ticket_type == "3" and self.amount < 2500 and self.ticket_date < datetime.date.today():
            self.validate = False

    def use_ticket(self):
        self.ticket_use_time = time.strftime("%H:%M:%S", time.localtime())
        if self.ticket_type != "1":
            self.amount = self.amount - 2500

    def save_tickets(self):
        with open("tickets.pkl", 'ab') as f:
            pickle.dump(self, f)

    @staticmethod
    def load_tickets():
        with open("tickets.pkl", 'rb') as file:
            while True:
                try:
                    yield pickle.load(file)
                except EOFError:
                    break

    @staticmethod
    def update_tickets(ticket_info):
        with open("tickets.pkl", 'wb') as file:
            for ticket in ticket_info:
                pickle.dump(ticket, file)


class Trip:
    """Class for creating trips"""

    def __init__(self, cost, start_time, end_time):
        self.cost = cost
        self.start_time = start_time
        self.end_time = end_time
        self.trip_validate = True
        logger_trip.info(f'{datetime.datetime.now()}: Trip class called ')


class User:
    id = 0
    user_registered = {}
    """User class for generate user and register in database
    :param id: like database primary key
    :param user_registered: a dictionary use as database
    """

    def __init__(self, user_name: str, password: str, phone_number: Optional[str] = None):
        """
        :param user_name:str, required, non duplicate
        :param password:str, minimum length 4 character
        :param phone_number: str, optional
        """
        self.username = user_name
        self.__password = password
        if not phone_number:
            self.phone_number = 'not present'
        else:
            self.phone_number = phone_number
        User.id += 1
        self.id = User.id
        User.user_registered[self.id] = self
        clear()
        print(f'{self.username} {GREEN}"registered"\n{END}')

    @staticmethod
    def __valid_pass(name_var: str, password: str) -> str:
        """
        check password validation and return sha256(password)
        :param name_var: variable name show in message
        :param password: user input password
        :return: str
        """
        try:
            assert len(str(password)) >= 4, f"{name_var} length should be longer than 3"
            return sha256(str(password).encode('utf-8')).hexdigest()
        except AssertionError as e:
            print(f'{YELLOW}("Hint:"){END}', e)

    @staticmethod
    def __valid_username(username: str) -> str:
        """
        check for non duplicated username
        :param username: str from user input
        :return: str
        """
        try:
            for _user in User.user_registered.values():
                assert username != _user.username, f'{username} already taken'
            else:
                return username
        except AssertionError as e:
            print(f'{YELLOW}("Hint:"){END}', e)

    @classmethod
    def register_new_user(cls, username: str, password: str, phone: str) -> None:
        """
        if username and password is valid call User class for initiate new User instance
        :param username: str form user input
        :param password: str from user input
        :param phone: str optional from user input
        :return: None
        """
        clear()
        print(f'{BLUE}========== register new user ==========\n{END}')
        if not username:
            print(f'{RED}Fail.{END}')
            print(f"{YELLOW}hint: " + f"username can't be empty{END}")
            return
        if not (user := cls.__valid_username(username)):
            print(f'{RED}Fail.{END}')
            return
        if not (passwd := cls.__valid_pass('password', password)):
            print(f'{RED}Fail.{END}')
            return
        phone = phone
        cls(user, passwd, phone)

    @staticmethod
    def login(_username: str, _password: str) -> None:
        """
        if _username and _password in database user authenticated
        :param _username: str from user input
        :param _password: str from user input
        :return: user
        """
        print(f'{BLUE}========== login ==========\n{END}')
        for __user in User.user_registered.values():
            if _username == __user.username and User.__valid_pass("password", _password) == __user.__password:
                return __user
        else:
            print(f'{RED}username or password incorrect.{END}')

    @staticmethod
    def change_password(_user: "User", _old_password: str, _new_password1=None, _new_password2=None):
        """
        change password if user old password and new password1 and 2 is valid
        :param _user: user object who want to change password
        :param _old_password: str from user input
        :param _new_password1: str from user input
        :param _new_password2: str from user input
        :return: None
        """
        print(f'{BLUE}========== change_password ==========\n{END}')

        _old_password = _user.__valid_pass("old_password", _old_password)
        if _old_password != _user.__password:
            print(f'> {RED}"your old password incorrect "{END} ')

            _new_password1 = _user.__valid_pass("new_password1", _new_password1)
            _new_password2 = _user.__valid_pass("new_password2", _new_password2)

            if _new_password1 != _new_password2 or not _new_password1 or not _new_password2:
                input(f'''> {RED}"your new password don't match or empty. press Enter to menu"{END} ''')
            return

        if _new_password1 != _new_password2 or not _new_password1 or not _new_password2:
            input(f'''> {RED}"your new password don't match or empty. press Enter to menu"{END} ''')
            return

        _new_password1 = _user.__valid_pass("new_password1", _new_password1)
        _new_password2 = _user.__valid_pass("new_password2", _new_password2)

        if _new_password1 and _new_password2:
            _user.__password = _new_password1
            User.user_registered[_user.id] = _user
            print(f'{GREEN}password change success.{END}')
            return

    def user_information(self):
        print(f'{BLUE}========== user information ==========\n{END}')
        print(self)

    def edit_username_and_phone(self, _username, _phone_number):
        """
        this method edit username and phone number
        :param _username: str from user input
        :param _phone_number: str from user input
        :return: None
        """
        print(f'{BLUE}========== edit username and phone ==========\n{END}')
        try:
            for user in User.user_registered.values():
                assert _username != user.username, f'{_username} already taken.'
        except AssertionError as e:
            print(f'{RED}{e}{END}')
            return

        if _username:
            self.username = _username

        if _phone_number == 'remove':
            self.phone_number = 'not present'
        elif _phone_number:
            self.phone_number = _phone_number

        User.user_registered[self.id] = self
        print(f'\n{GREEN}username and phone number edit successful.\n')

    def __str__(self):
        return f'username: {self.username}\nphone: {self.phone_number}\n'

    def __repr__(self):
        return f'username: {self.username}\nphone: {self.phone_number}\npassword: hashed'


class BankAccount:

    WAGE_AMOUNT = 600
    MIN_BALANCE = 10000

    """
    Class for creating bank account using it
    :param WAGE_AMOUNT: Wage of some actions
    :param MIN_BALANCE: The minimum amount of account
    """

    class MinBalanceError(Exception):
        pass

    def __init__(self, owner: User, initial_balance: int = 0) -> None:
        self.__owner = owner
        self.__balance = initial_balance

    def __check_minimum_balance(self, amount_to_withdraw):
        return (self.__balance - amount_to_withdraw) >= self.MIN_BALANCE

    def set_owner(self, owner):
        self.__owner = owner

    def get_owner(self):
        return self.__owner

    def withdraw(self, amount):
        if self.__check_minimum_balance(amount):
            raise BankAccount.MinBalanceError("NOT Enough balance to withdraw!")
        self.__balance -= amount
        self.__balance -= self.WAGE_AMOUNT

    def deposit(self, amount):
        self.__balance += amount

    def get_balance(self):
        self.__balance -= self.WAGE_AMOUNT
        return self.__balance

    def transfer(self, target_account, amount: int):
        self.withdraw(amount)
        target_account.deposit(amount)

    @classmethod
    def change_wage(cls, new_amount):
        cls.WAGE_AMOUNT = max(new_amount, 0)

    @classmethod
    def change_min_balance(cls, new_amount):
        cls.MIN_BALANCE = max(new_amount, 0)


main_menu = {
    '1': 'manager',
    '2': 'passenger',
    '0': 'exit'
}
passenger_menu = {
    '1': 'register new user',
    '2': 'login',
    '3': 'main menu'
}
_authenticated_menu = {
    '1': 'user information',
    '2': 'edit username and phone',
    '3': 'change password',
    '4': 'by ticket',
    '5': 'logout'
}
manager_menu = {
    '1': 'register new manager',
    '2': 'login',
    '3': 'main menu'
}
control_panel = {
    '5': 'logout'
}


def clear():
    """Function for clearing the terminal, based on the user's OS"""

    if platform.system() == "Linux":
        os.system("clear")
    if platform.system() == "Windows":
        os.system("cls")


def print_menu(_menu):
    """Function for printing the menus"""

    for item in _menu:
        print(f'{item}: {_menu[item]}')


if __name__ == "__main__":
    def menu():
        clear()
        while True:
            clear()
            print(f"{BLUE}============ Welcome to metro app ============\n{END}")
            print_menu(main_menu)

            action = input('\n> ')

            if action == '0':
                print('good bye see you soon')
                sys.exit()

            _action = main_menu.get(action)

            if _action == 'manager':
                clear()
                manager()
            elif _action == 'passenger':
                clear()
                passenger()
            else:
                input(f'> {RED}"invalid input, press Enter to continue..." {END}')
                clear()

    def manager():
        while True:
            print(f"{BLUE}============ manager menu ============\n{END}")
            print_menu(manager_menu)

            action = input('\n> ')

            if action == '3':
                menu()

            op = manager_menu.get(action)

            if op == 'register new manager':
                fullname = input("> full_name: ")
                password = input("> password: ")
                number = input("> mobile: ")
                Manager.register_new_manager(fullname, password, number)
            elif op == 'login':
                fullname = input("> full_name: ")
                _password = input("> _password: ")
                if manager := Manager.login(fullname, _password):
                    print(f'\n{GREEN}login success.{END}')
                    print(f'{GREEN}welcome {fullname}\n{END}')
                    while True:
                        print(f'{BLUE}============ control panel ============\n{END}')
                        print_menu(control_panel)
                        _user_input = input('\n> ')
                        _op = control_panel.get(_user_input)
                        if _op:
                            _op = _op.replace(' ', '_')
                        if _op == 'logout':
                            clear()
                            print('good bye')
                            break
                        elif _op == 'change_password':
                            old_password = input("> old password [leave empty for exit]: ")
                            if not old_password:
                                continue
                            else:
                                new_password1 = input("> new password")
                                new_password2 = input("> repeat password")
                                User.change_password(manager, old_password, new_password1, new_password2)
                        elif _op == 'edit_full_name_and_phone':
                            _username = input(f'> new username [leave empty for {manager.full_name}]: ')
                            _phone_number = input(f'> new phone number: [leave empty for {manager.phone_number}]\n'
                                                  f' or type {YELLOW}"remove"{END} ' + 'for remove your phone number: ')
                            manager.edit_fullname_and_phone(_username, _phone_number)
                        elif _op:
                            exec(f'user.{_op}()')
                        else:
                            input(f'> {RED}"invalid input, press Enter to continue..." {END}')
                            clear()
            else:
                input(f'> {RED}"invalid input, press Enter to continue..." {END}')
                clear()


    def passenger():
        while True:
            print(f'{BLUE}============ passenger menu ============\n{END}')
            print_menu(passenger_menu)

            action = input('\n> ')

            if action == '3':
                menu()

            op = passenger_menu.get(action)

            if op == 'register new user':
                username = input("> username: ")
                password = input("> password: ")
                phone = input("> mobile: ")
                User.register_new_user(username, password, phone)
            elif op == 'login':
                username = input("> username: ")
                password = input("> password: ")
                if user := User.login(username, password):
                    print(f'\n{GREEN}login success.{END}')
                    print(f'{GREEN}welcome {username}\n{END}')
                    while True:
                        print(f'{BLUE}============ user authenticated menu ============\n{END}')
                        print_menu(_authenticated_menu)
                        _user_input = input('\n> ')
                        _op = _authenticated_menu.get(_user_input)
                        if _op:
                            _op = _op.replace(' ', '_')
                        if _op == 'logout':
                            print('good by')
                            break
                        elif _op == 'change_password':
                            old_password = input("> old password [leave empty for exit]: ")
                            if not old_password:
                                continue
                            else:
                                new_password1 = input("> new password")
                                new_password2 = input("> repeat password")
                                User.change_password(user, old_password, new_password1, new_password2)
                        elif _op == 'edit_username_and_phone':
                            _username = input(f'> new username [leave empty for {user.user_name}]: ')
                            _phone_number = input(f'> new phone number: [leave empty for {user.phone_number}]\n'
                                                  f' or type {YELLOW}"remove"{END} ' + 'for remove your phone number: ')
                            user.edit_username_and_phone(_username, _phone_number)
                        elif _op:
                            exec(f'user.{_op}()')
                        else:
                            input(f'> {RED}"invalid input, press Enter to continue..." {END}')
                            clear()
            else:
                input(f'> {RED}"invalid input, press Enter to continue..." {END}')
                clear()


    menu()
