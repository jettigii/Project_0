from flask import jsonify, request

from services.banking_service import BankingService
from daos.bank_dao import BankDAO
from models.client import Client
from models.account import Account


def route(app):
    bank_dao = BankDAO()

    @app.route("/")
    def hello():
        return "<h1>Welcome to Morshu's Bank!</h1>Remember, Morshu doesn't give credit."

    # CLIENT TIME  #######################################################

    # CREATE CLIENT     ✓
    @app.route("/clients", methods=['POST', 'GET'])
    def create_clients():
        if request.method == 'POST':
            new_client = bank_dao.create_client()
            if new_client:
                return jsonify(new_client), 201
            else:
                return "could not create a new client", 503
    # GET ALL CLIENTS   ✓
        elif request.method == 'GET':
            all_clients = bank_dao.all_clients()
            if all_clients:
                return jsonify(bank_dao.all_clients()), 200
            else:
                return "could not get all the clients", 503
            # try:
            #     return jsonify(bank_dao.all_clients()), 200
            # except:
            #     return "could not get all the clients", 503

    # GET A CLIENT      ✓
    @app.route("/clients/<client_id>", methods=['GET'])
    def get_client(client_id):

        client = bank_dao.get_client(client_id)
        if len(client) > 0:
            return jsonify(client), 200
        else:
            return "could not find the user id", 404

    # UPDATE A CLIENT   ✓
    @app.route("/clients/<client_id>", methods=['PUT'])
    def update_client(client_id):
        try:
            name = request.args['name']
            account_ids = request.args['account_ids']
            update = bank_dao.update_client(client_id, name, account_ids)

            if update:
                return jsonify(update), 205
            else:
                return "could not find the user id to update", 404
        except:
            return "could not find the user id to update", 404

    # DELETE A CLIENT   ✓
    @app.route("/clients/<client_id>", methods=['DELETE'])
    def delete_client(client_id):
        if bank_dao.delete_client(client_id):
            return "deleted the user id", 205
        else:
            return "could not find the user id to delete", 404



