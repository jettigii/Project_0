from flask import jsonify, request

from services.banking_service import BankingService
from daos.bank_dao import BankDAO
from models.client import Client
from models.account import Account


def route(app):
    bank_dao = BankDAO()
    # ACCOUNT TIME  #######################################################

    # CREATE new ACCOUNT for a Client   ✓
    @app.route("/clients/<client_id>/accounts", methods=['POST', 'GET'])
    def create_account(client_id):
        if request.method == 'POST':
            new_account = bank_dao.create_client_account(client_id)
            if new_account:
                return jsonify(new_account), 201
            else:
                return "could not create a new account", 503

        # GET ALL of a CLIENT's Accounts   ✓
        elif request.method == 'GET':
            client_account_list = bank_dao.all_client_accounts(client_id)

            if client_account_list:
                less_than = -1
                greater_than = -1
                try:
                    less_than = int(request.args['amountLessThan'])
                    greater_than = int(request.args['amountGreaterThan'])
                except:
                    pass
                if less_than >= 0 and greater_than >= 0:
                    between_clients = bank_dao.get_account_between(less_than, greater_than, client_account_list)
                    if between_clients:
                        return jsonify(between_clients), 200
                    else:
                        return "could not get all the clients accounts in between", 404
                else:
                    return jsonify(bank_dao.all_client_accounts(client_id)), 200
            else:
                return "could not get all the clients accounts", 404

    # GET A CLIENTS ACCOUNT BY a client and an account ID
    @app.route("/clients/<client_id>/accounts/<account_id>", methods=['GET', 'PUT', 'DELETE', 'PATCH'])
    def get_account(client_id, account_id):
        if request.method == 'GET':
            account = bank_dao.get_client_account(client_id, account_id)
            if account:
                return jsonify(account), 200
            else:
                return "could not find the user id or account id", 404
        elif request.method == 'PUT':
            type_id = 0
            worth = 0
            try:
                type_id = int(request.args['typeID'])
                worth = float(request.args['worth'])

                account = bank_dao.update_client_account(client_id, account_id, type_id, worth)
                if account:
                    return jsonify(account), 200
                else:
                    return "could not find the user id or account id", 404
            except:
                return "could not find the user id or account id *", 404

        elif request.method == 'DELETE':
            account = bank_dao.delete_client_account(client_id, account_id)
            if account:
                return "deleted account id: " + str(account_id), 200
            else:
                return "could not find the user id or account id", 404

        elif request.method == 'PATCH':
            deposit = 0
            withdraw = 0
            try:
                deposit = float(request.args['deposit'])
                print(deposit)
            except: pass
            try:
                withdraw = float(request.args['withdraw'])
                print(withdraw)
            except: pass

            try:
                prev_message = ""
                if deposit > 0:
                    deposit_transfer = bank_dao.deposit_client_account(client_id, account_id, deposit)
                    if deposit_transfer:
                        if withdraw == 0:
                            return "deposited $" + str(deposit) + " into the account", 201
                        else:
                            prev_message = "deposited $" + str(deposit) + " into the account"
                    else:
                        return "could not find the client or account(s)", 404

                if withdraw > 0:
                    deposit_transfer = bank_dao.withdraw_client_account(client_id, account_id, withdraw)
                    if deposit_transfer:
                        if deposit_transfer == 2:
                            return "could not withdraw $" + str(
                                withdraw) + " from the account, Insufficient Funds", 422
                        if prev_message != "":
                            return prev_message + "\nwithdrew $" + str(withdraw) + " from the account", 201
                        else:
                            return "withdrew $" + str(withdraw) + " from the account", 201
                    else:
                        return "could not find the client or account(s)", 404

                return "could not complete the operation", 404
            except:
                return "could not find the user id or account id *", 404

    # Transfer from ACCOUNT to other account
    @app.route("/clients/<client_id>/accounts/<account_id>/transfer/<account_id2>", methods=['PATCH'])
    def transfer_account(client_id, account_id, account_id2):
        amount = 0
        try:
            amount = float(request.args['amount'])
            # print(amount, client_id, account_id, account_id2)
            transfer = bank_dao.transfer_client_accounts(client_id, account_id, account_id2, amount)
            if transfer:
                if transfer == 2:
                    return "could not transfer $" + str(amount) + " to the account, Insufficient Funds", 422
                return "transferred $" + str(amount) + " to the account", 201
            else:
                return "could not find the client or account(s)", 404
        except:
            return "could not find the user id or account id *", 404

