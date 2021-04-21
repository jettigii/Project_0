
class Client:
    def __init__(self, client_id=0, name="", account_id=[]):
        self.client_id = client_id
        self.name = name
        self.account_id = account_id

    def json(self):
        return {
            'clientID': self.client_id,
            'name': self.name,
            'accountID': self.account_id
        }

    @staticmethod
    def json_parse(json):
        client = Client()
        client.client_id = json["clientID"]
        client.name = json["name"],
        client.account_id = json["accountID"]

        return client
