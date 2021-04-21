from daos.bank_dao import BankDAO
from util import logger


class BankingService:
    bank_dao = BankDAO()

    @classmethod
    def create_client(cls, client):
        pass

    @classmethod
    def delete_client(cls, client):
        pass

    @classmethod
    def all_clients(cls):
        return cls.banking_dao.all_clients()

    @classmethod
    def get_client(cls, client_id):
        pass

    @classmethod
    def update_client(cls, client_id, client_name, client_account_ids):
        return cls.banking_dao.update_movie(client_id, client_name, client_account_ids)
