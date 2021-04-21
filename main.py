# Project 0

from flask import Flask
from controllers import main_controller
from util.logger import log
from daos.bank_dao import BankDAO as bd

app = Flask(__name__)
main_controller.route(app)

if __name__ == '__main__':
    log()
    app.run()
    pass

