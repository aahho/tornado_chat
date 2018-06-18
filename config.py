# -*- coding: utf-8 -*-

import os
import pymongo
from wrappers.mongodb import MongoDBWrapper

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATABASES = {
	'mongo': {
		'ENGINE': pymongo.MongoClient('localhost', 27017),
		'NAME': 'CHAT_APP',
		'HOST': 'localhost',
		'PORT': 27017,
		'WRAPPER': MongoDBWrapper()
	},
	'postgres': {
		'ENGINE': 'pycopg2',
		'NAME': 'chat_app',
		'USER': 'postgres',
		'PASSWORD': 'postgres',
		'HOST': 'localhost',
		'PORT': '5432',
	}
}