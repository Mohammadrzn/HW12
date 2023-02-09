from hashlib import sha256
from main import clear
from main import User
import logging

logger_admin = logging.getLogger('metro')

RED = "\033[0;31m"
GREEN = "\033[0;32m"
BLUE = "\033[0;34m"
YELLOW = "\033[1;33m"
END = "\033[0m"


class Manager:
    registered = {}
    """
    Class for creating manager
    :param registered: a dictionary use as database
    """

    def __init__(self, full_name: str, password: str, number: str):
        """
        :param full_name:str, required
        :param password:str, minimum length 5 character
        :param number: str,
        """
        self.full_name = full_name
        self.number = number
        self.__password = password
        clear()
        print(f'{self.full_name} {GREEN}"registered"\n{END}')

    @staticmethod
    def __valid_pass(name_var: str, password: str):
        """
        check password validation and return sha256(password)
        :param name_var: variable name show in message
        :param password: user input password
        :return: str
        """
        try:
            assert len(str(password)) >= 5, f"{name_var} length should be at least 5 characters"
            return sha256(str(password).encode('utf-8')).hexdigest()
        except AssertionError as e:
            print(f'{YELLOW}("Hint:"){END}', e)

    @classmethod
    def register_new_manager(cls, fullname: str, password: str, phone: str):
        """
        if password is valid call Manager class for initiate new manager instance
        :param fullname: str form user input
        :param password: str from user input
        :param phone: str from user input
        """
        print(f'{BLUE}========== register new manager ==========\n{END}')
        if not fullname:
            print(f"{YELLOW}hint: " + "full name can't be empty{END}")
            print(f'{RED}Fail.{END}')
            return
        if not (passwd := cls.__valid_pass('password', password)):
            print(f'{RED}Fail.{END}')
            return
        phone = phone
        cls(fullname, passwd, phone)

    @staticmethod
    def login(_fullname: str, _password: str):
        """
        if _username and _password in database user authenticated
        :param _fullname: str from user input
        :param _password: str from user input
        :return: user
        """
        print(f'{BLUE}========== login ==========\n{END}')
        for __name in Manager.registered.values():
            if _fullname == __name.fullname and Manager.__valid_pass("password", _password) == __name.__password:
                return __name
        else:
            clear()
            print(f'{RED}full name or password incorrect.{END}')

    @staticmethod
    def change_password(_manager: 'manager', _old_password: str, _new_password1=None, _new_password2=None):
        """
        change password if manager old password and new password1 and password2 is valid
        :param _manager: user object who want to change password
        :param _old_password: str from input
        :param _new_password1: str from input
        :param _new_password2: str from input
        :return: None
        """
        print(f'{BLUE}========== change_password ==========\n{END}')
        _old_password = _manager.__valid_pass("old_password", _old_password)
        if _old_password != _manager.__password:
            print(f'> {RED}"your old password is incorrect "{END} ')

            _new_password1 = _manager.__valid_pass("new_password1", _new_password1)
            _new_password2 = _manager.__valid_pass("new_password2", _new_password2)

            if _new_password1 != _new_password2 or not _new_password1 or not _new_password2:
                input(f'''> {RED}"your new password don't match or empty. press Enter to menu"{END} ''')
            return
        if _new_password1 != _new_password2 or not _new_password1 or not _new_password2:
            input(f'''> {RED}"your new password don't match or empty. press Enter to menu"{END} ''')
            return
        _new_password1 = _manager.__valid_pass("new_password1", _new_password1)
        _new_password2 = _manager.__valid_pass("new_password2", _new_password2)
        if _new_password1 and _new_password2:
            _manager.__password = _new_password1
            User.user_registered[_manager.id] = _manager
            print(f'{GREEN}password change success.{END}')
            return

    def manager_information(self):
        print(f'{BLUE}========== manager information ==========\n{END}')
        print(self)

    def edit_fullname_and_phone(self, _fullname, _phone_number):
        """
        this method edits full name and phone number
        :param _fullname: str from user input
        :param _phone_number: str from user input
        :return: None
        """
        print(f'{BLUE}========== edit full name and mobile ==========\n{END}')
        try:
            for manager in Manager.registered.values():
                assert _fullname != manager.username, f'{_fullname} already taken.'
        except AssertionError as e:
            print(f'{RED}{e}{END}')
            return

        if _fullname:
            self.full_name = _fullname
        if _phone_number == 'remove':
            self.number = 'not present'
        elif _phone_number:
            self.number = _phone_number

        print(f'\n{GREEN}username and phone number edit successful.\n')

    def __str__(self):
        return f'username: {self.full_name}\nphone: {self.number}\n'

    def __repr__(self):
        return f'username: {self.full_name}\nphone: {self.number}\npassword: hashed'
