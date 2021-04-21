from flask import Flask
from controllers import clients_controller as cc
from controllers import accounts_controller as ac


def route(app):
    cc.route(app)
    ac.route(app)
