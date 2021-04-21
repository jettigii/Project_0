import unittest
from daos.bank_dao import BankDAO as bd


class TestAccountsController(unittest.TestCase):

    # ACCOUNTS ------------------------------------------------------

    # 6. creates a new account for client with the id of 1
    def test_create_new_account_success(self):
        assert bd.create_client_account(bd, 1)

    # 7. get all accounts for client 1
    def test_get_all_accounts_for_client_success(self):
        assert bd.all_client_accounts(bd, 1)

    # 8. get all accounts for client 2 between 400 and 2000
    def test_get_all_accounts_for_client_in_range_success(self):
        assert bd.get_account_between(bd, 9999999, 0, bd.all_client_accounts(bd, 1))

    # 9. get account 1 for client 1
    def test_get_account_success(self):
        assert bd.get_client_account(bd, 1, 1)

    # 10. update account with the id 1 for client 1
    def test_update_account_success(self):
        assert bd.update_client_account(bd, 1, 1, 1, 1000000)

    # 11. delete account 2 for client 3
    def test_delete_account_success(self):
        assert bd.delete_client_account(bd, 3, 2)

    # 12. Withdraw/deposit given amount (Body: {"deposit":500} or {"withdraw":250})
    def test_deposit_success(self):
        assert bd.deposit_client_account(bd, 1, 1, 500)

    def test_withdraw_success(self):
        assert bd.withdraw_client_account(bd, 1, 1, 500500)

    # 13. transfer funds from account 7 to account 8
    def test_transfer_success(self):
        assert bd.transfer_client_accounts(bd, 1, 1, 3, 50)


if __name__ == '__main__':
    unittest.main()
