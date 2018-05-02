from flask import Flask, request, jsonify, Blueprint
from flaskext.mysql import MySQL
qrserver = Blueprint('qrserver', __name__)
