# -*- coding: utf-8 -*-
'''
Create on 2016-12-14

author bhy
'''
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
basedir= os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] =True
SQLAlchemyDB = SQLAlchemy(app)

from app.database import model