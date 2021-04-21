import unittest
from daos.bank_dao import BankDAO as bd


class TestClientsController(unittest.TestCase):

    # 1. Creates a new client
    def test_create_new_client_success(self):
        assert bd.create_client(bd)

    # 2. gets all clients
    def test_get_all_clients_success(self):
        assert bd.all_clients(bd)

    # 3. get client with id of 1
    def test_get_a_client_success(self):
        assert bd.get_client(bd, 1)

    # 4. updates client with id of 1
    def test_update_client_success(self):
        assert bd.update_client(bd, 1, "Sharon Is. Karen", "{2,5,6}")

    # 5. deletes client with the id of #
    def test_delete_client_success(self):
        assert bd.delete_client(bd, 5)


if __name__ == '__main__':
    unittest.main()
