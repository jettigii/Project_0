from abc import abstractmethod, ABC
import psycopg2
from psycopg2._psycopg import connection
import util.db_connections as db
from models.client import Client
from models.account import Account
import names


class BankDAO:

    @abstractmethod
    def create_client(self):
        try:
            # insert into client values (default, 'Manfred', '{1}');
            sql = "INSERT INTO client VALUES (DEFAULT,%s,'{}') returning *"
            cursor = db.get_connected_for_free.cursor()
            cursor.execute(sql, [names.get_full_name()])
            db.get_connected_for_free.commit()
            client_tmp = cursor.fetchone()
            client = Client(client_tmp[0], client_tmp[1], client_tmp[2]).json()
            return client
        except:
            return False

    @abstractmethod
    def get_client(self, client_id):
        try:
            sql = "SELECT * FROM client WHERE id = %s"
            cursor = db.get_connected_for_free.cursor()
            cursor.execute(sql, [client_id])
            records = cursor.fetchall()

            client_list = []

            for record in records:
                client = Client(record[0], record[1], record[2])
                client_list.append(client.json())

            return client_list
        except:
            return False

    @abstractmethod
    def all_clients(self):
        try:
            sql = "SELECT * FROM client"
            cursor = db.get_connected_for_free.cursor()
            cursor.execute(sql)
            records = cursor.fetchall()

            client_list = []

            for record in records:
                client = Client(record[0], record[1], record[2])
                client_list.append(client.json())

            return client_list
        except:
            return False

    @abstractmethod
    def update_client(self, client_id, client_name, client_account_ids):

        check = 0

        try:
            check = len(self.get_client(client_id))
        except:
            try:
                check = len(self.get_client(self, client_id))
            except:
                return False

        if check > 0:
            sql = "update client set name = %s, account_ids = %s where id = %s returning *"
            cursor = db.get_connected_for_free.cursor()
            cursor.execute(sql, (client_name, client_account_ids, client_id))
            db.get_connected_for_free.commit()
            client_tmp = cursor.fetchone()
            client = Client(client_tmp[0], client_tmp[1], client_tmp[2]).json()
            return client
        else:
            return False

    @abstractmethod
    def delete_client(self, client_id):

        check = 0

        try:
            check = len(self.get_client(client_id))
        except:
            try:
                check = len(self.get_client(self, client_id))
            except:
                return False

        if check > 0:
            sql = "DELETE FROM client WHERE id = %s"
            cursor = db.get_connected_for_free.cursor()
            cursor.execute(sql, [client_id])
            db.get_connected_for_free.commit()
            return True
        else:
            return False

    # ------------------------------------------------------------------------------------------------------------------

    # Get clients account arrays
    @abstractmethod
    def get_client_accounts(self, client_id):
        sql = "SELECT account_ids FROM client WHERE id = %s"
        cursor = db.get_connected_for_free.cursor()
        cursor.execute(sql, [client_id])
        records = cursor.fetchall()

        account_list = []

        for record in records:
            account_list.append(record)

        return "(" + str(str(account_list).replace('[', '').replace(']', '').replace('(', '').replace(')', '').replace(' ', '')[0:-1]) + ")"

    # ---------------------------------------------------------------------

    @abstractmethod
    def create_client_account(self, clientID):
        clientID = str(clientID)

        try:
            # Create new account
            sql = "INSERT INTO account VALUES (DEFAULT,1,'0') RETURNING id"
            cursor = db.get_connected_for_free.cursor()
            cursor.execute(sql)
            new_id = cursor.fetchone()[0]
            db.get_connected_for_free.commit()
            # insert into client id account
            sql = "update client set account_ids = array_append(account_ids, " + str(new_id) + ") where id = %s"
            cursor = db.get_connected_for_free.cursor()
            cursor.execute(sql, clientID)
            db.get_connected_for_free.commit()
            # return new account
            sql = "SELECT * FROM account WHERE id = %s"
            cursor = db.get_connected_for_free.cursor()
            cursor.execute(sql, [new_id])

            account_tmp = cursor.fetchone()
            account = Account(account_tmp[0], account_tmp[1], account_tmp[2]).json()
            return account
        except psycopg2.errors.ForeignKeyViolation:
            cursor.execute("ROLLBACK")
            return False

    @abstractmethod
    def all_client_accounts(self, client_id):

        account_str_list = "()"
        try:
            account_str_list = str(self.get_client_accounts(client_id))
        except:
            try:
                account_str_list = str(self.get_client_accounts(self, client_id))
            except:
                return False

        # print(account_str_list)
        if account_str_list == "()":
            return False

        sql = "SELECT * FROM account WHERE id in " + account_str_list

        cursor = db.get_connected_for_free.cursor()
        cursor.execute(sql)
        records = cursor.fetchall()

        account_list = []

        for record in records:
            account = Account(record[0], record[1], record[2])
            account_list.append(account.json())

        if len(account_list) > 0:
            return account_list
        else:
            return False

    @abstractmethod
    def get_client_account(self, client_id, account_id):
        sql = "SELECT * FROM client WHERE id = %s"
        cursor = db.get_connected_for_free.cursor()
        cursor.execute(sql, [client_id])
        records = cursor.fetchall()

        client_list = []

        for record in records:
            client = Client(record[0], record[1], record[2])
            client_list.append(client.json())

        if len(client_list) > 0:
            if str(account_id) in str(Client.json_parse(client_list[0]).account_id):
                sql = "SELECT * FROM account WHERE id = %s"
                cursor = db.get_connected_for_free.cursor()
                cursor.execute(sql, [account_id])
                records = cursor.fetchall()

                account_list = []

                for record in records:
                    account = Account(record[0], record[1], record[2])
                    account_list.append(account.json())
                if len(account_list) > 0:
                    return account_list
                else:
                    return False
            else:
                return False
        else:
            return False

    @abstractmethod
    def get_account_between(self, less_than, greater_than, client_account_list):

        account_list = []

        for record in client_account_list:
            # account = Account(record[0], record[1], record[2])
            account_list.append(Account.json_parse(record))

        account_list_between = []

        for record in account_list:
            # print(int(record.worth[1:-3].replace(',', '')))
            if int(greater_than) < int(record.worth[1:-3].replace(',', '')) < int(less_than):
                account_list_between.append(record.json())
                print(int(record.worth[1:-3].replace(',', '')))

        if len(account_list_between) > 0:
            return account_list_between
        else:
            return False

        # return False

    @abstractmethod
    def delete_client_account(self, client_id, account_id):
        sql = "SELECT * FROM client WHERE id = %s"
        cursor = db.get_connected_for_free.cursor()
        cursor.execute(sql, [client_id])
        records = cursor.fetchall()

        client_list = []

        for record in records:
            client = Client(record[0], record[1], record[2])
            client_list.append(client.json())

        if len(client_list) > 0:
            if str(account_id) in str(Client.json_parse(client_list[0]).account_id):
                # Delete from account table
                sql = "DELETE FROM account WHERE id = %s"
                cursor = db.get_connected_for_free.cursor()
                cursor.execute(sql, [account_id])
                db.get_connected_for_free.commit()

                # Delete from client account list
                sql = "update client set account_ids = array_remove(account_ids, %s) where id = %s"
                cursor = db.get_connected_for_free.cursor()
                cursor.execute(sql, (account_id, client_id))
                db.get_connected_for_free.commit()
                return True
            else:
                return False
        else:
            return False

    @abstractmethod
    def update_client_account(self, client_id, account_id, type_id, worth):
        sql = "SELECT * FROM client WHERE id = %s"
        cursor = db.get_connected_for_free.cursor()
        cursor.execute(sql, [client_id])
        records = cursor.fetchall()

        client_list = []

        for record in records:
            client = Client(record[0], record[1], record[2])
            client_list.append(client.json())

        if str(account_id) in str(Client.json_parse(client_list[0]).account_id):
            if len(client_list) > 0:
                check = 0

                try:
                    check = len(self.get_client(client_id))
                except:
                    try:
                        check = len(self.get_client(self, client_id))
                    except:
                        return False

                if check > 0:
                    sql = "update account set type_id = %s, worth = %s where id = %s RETURNING *"
                    cursor = db.get_connected_for_free.cursor()
                    cursor.execute(sql, (type_id, worth, account_id))
                    db.get_connected_for_free.commit()

                    account_tmp = cursor.fetchone()
                    account = Account(account_tmp[0], account_tmp[1], account_tmp[2]).json()
                    return account
                else:
                    return False
            else:
                return False
        else:
            return False

    @abstractmethod
    def transfer_client_accounts(self, client_id, account_id, account_id2, amount):
        # check for client id
        sql = "SELECT * FROM client WHERE id = %s"
        cursor = db.get_connected_for_free.cursor()
        cursor.execute(sql, [client_id])
        records = cursor.fetchall()

        client_list = []

        for record in records:
            client = Client(record[0], record[1], record[2])
            client_list.append(client.json())

        # check for account id
        sql = "SELECT * FROM account WHERE id = %s"
        cursor = db.get_connected_for_free.cursor()
        cursor.execute(sql, [account_id])
        records = cursor.fetchall()

        account_list1 = []

        for record in records:
            account = Account(record[0], record[1], record[2])
            account_list1.append(client.json())

        # check for account id2
        sql = "SELECT * FROM account WHERE id = %s"
        cursor = db.get_connected_for_free.cursor()
        cursor.execute(sql, [account_id2])
        records = cursor.fetchall()

        account_list2 = []

        for record in records:
            account = Account(record[0], record[1], record[2])
            account_list2.append(client.json())

        # Get amount from account 1
        sql = "SELECT worth FROM account WHERE id = %s"
        cursor = db.get_connected_for_free.cursor()
        cursor.execute(sql, [account_id])
        worth = cursor.fetchone()[0]

        worth = float(str(worth).replace('$', '').replace(',', ''))
        # print(worth, amount)
        if worth >= amount:
            if str(account_id) in str(Client.json_parse(client_list[0]).account_id):
                if len(client_list) > 0 and len(account_list1) > 0 and len(account_list2) > 0:
                    check = 0

                    try:
                        check = len(self.get_client(client_id))
                    except:
                        try:
                            check = len(self.get_client(self, client_id))
                        except:
                            return False
                    if check > 0:
                        # Add money to account2
                        sql = "update account set worth = (%s+worth::decimal) where id = %s"
                        cursor = db.get_connected_for_free.cursor()
                        cursor.execute(sql, (amount, account_id2))
                        db.get_connected_for_free.commit()
                        # Subtract money from account
                        sql = "update account set worth = (worth::decimal-%s) where id = %s"
                        cursor = db.get_connected_for_free.cursor()
                        cursor.execute(sql, (amount, account_id))
                        db.get_connected_for_free.commit()
                        return True
                    else:
                        return False
                else:
                    return False
            else:
                return False
        else:
            return 2

    @abstractmethod
    def deposit_client_account(self, client_id, account_id, amount):
        sql = "SELECT * FROM client WHERE id = %s"
        cursor = db.get_connected_for_free.cursor()
        cursor.execute(sql, [client_id])
        records = cursor.fetchall()

        client_list = []

        for record in records:
            client = Client(record[0], record[1], record[2])
            client_list.append(client.json())

        if str(account_id) in str(Client.json_parse(client_list[0]).account_id):
            if len(client_list) > 0:
                check = 0

                try:
                    check = len(self.get_client(client_id))
                except:
                    try:
                        check = len(self.get_client(self, client_id))
                    except:
                        return False

                if check > 0:
                    sql = "update account set worth = %s+worth::decimal where id = %s"
                    cursor = db.get_connected_for_free.cursor()
                    cursor.execute(sql, (amount, account_id))
                    db.get_connected_for_free.commit()
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False

    @abstractmethod
    def withdraw_client_account(self, client_id, account_id, amount):
        # check for client id
        sql = "SELECT * FROM client WHERE id = %s"
        cursor = db.get_connected_for_free.cursor()
        cursor.execute(sql, [client_id])
        records = cursor.fetchall()

        client_list = []

        for record in records:
            client = Client(record[0], record[1], record[2])
            client_list.append(client.json())

        # check for account id
        sql = "SELECT * FROM account WHERE id = %s"
        cursor = db.get_connected_for_free.cursor()
        cursor.execute(sql, [account_id])
        records = cursor.fetchall()

        account_list1 = []

        for record in records:
            account = Account(record[0], record[1], record[2])
            account_list1.append(client.json())

        # Get amount from account 1
        sql = "SELECT worth FROM account WHERE id = %s"
        cursor = db.get_connected_for_free.cursor()
        cursor.execute(sql, [account_id])
        worth = cursor.fetchone()[0]

        worth = float(str(worth).replace('$', '').replace(',', ''))
        # print(worth, amount)
        if worth >= amount:
            if str(account_id) in str(Client.json_parse(client_list[0]).account_id):
                if len(client_list) > 0 and len(account_list1) > 0:
                    check = 0

                    try:
                        check = len(self.get_client(client_id))
                    except:
                        try:
                            check = len(self.get_client(self, client_id))
                        except:
                            return False
                    if check > 0:
                        # Subtract money from account
                        sql = "update account set worth = (worth::decimal-%s) where id = %s"
                        cursor = db.get_connected_for_free.cursor()
                        cursor.execute(sql, (amount, account_id))
                        db.get_connected_for_free.commit()
                        return True
                    else:
                        return False
                else:
                    return False
            else:
                return False
        else:
            return 2