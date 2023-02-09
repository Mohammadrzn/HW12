from datetime import *
import logging
import pickle
import main

logger_admin = logging.getLogger('metro')


class Admin(main.User):
    def __init__(self, first_name, last_name, phone_number, _id):
        super().__init__(first_name, last_name, phone_number)
        self.admin_id = _id
        logger_admin.info(f'{datetime.now()}: Admin class called')

    def save_admins(self):
        with open("admins.pkl", 'ab') as db:
            pickle.dump(self, db)

    @staticmethod
    def load_admins():
        with open("admin.pkl", 'rb') as file:
            while True:
                try:
                    yield pickle.load(file)
                except EOFError:
                    break

    @staticmethod
    def update_admins(admins_info_list):
        with open("admins.pkl", 'wb') as f:
            for admin in admins_info_list:
                pickle.dump(admin, f)
