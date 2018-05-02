from flask import Flask, request, jsonify, Blueprint
from flaskext.mysql import MySQL
manageShareholder = Blueprint('manageShareholder', __name__)
