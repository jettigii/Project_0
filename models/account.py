
class Account:
    def __init__(self, account_id=0, account_type="", worth=0):
        self.account_id = account_id
        self.account_type = account_type
        self.worth = worth

    def json(self):
        return {
            'accountID': self.account_id,
            'accountType': self.account_type,
            'worth': self.worth
        }

    @staticmethod
    def json_parse(json):
        account = Account()
        account.account_id = json["accountID"]
        account.account_type = json["accountType"],
        account.worth = json["worth"]

        return account
