from flask import Flask, request, jsonify, Blueprint
from flaskext.mysql import MySQL
manageAgenda = Blueprint('manageAgenda', __name__)
