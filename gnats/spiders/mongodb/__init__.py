__author__ = 'tchen'

from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.gnats
issues = db['issues']