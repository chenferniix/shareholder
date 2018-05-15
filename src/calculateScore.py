#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, request, jsonify, Blueprint
from flaskext.mysql import MySQL
from src.sql import *
calculateScore = Blueprint('calculateScore', __name__)

@calculateScore.route("/calculateScoreAgenda/<uuid>",methods=['post'])
def calculateScoreAgenda(uuid):
    return ""
