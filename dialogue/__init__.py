# -*- coding: utf-8 -*-
'''
Create on 2016-12-14

author bhy
'''
import os
from common import instance
from flask_sqlalchemy import SQLAlchemy

basedir= os.path.abspath(os.path.dirname(__file__))
instance.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir,'data.sqlite')
instance.app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] =True
SQLAlchemyDB = SQLAlchemy(instance.app)