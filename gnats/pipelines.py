# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html
from datetime import datetime

from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.gnats
issues = db['issues']


class MongoPipeline(object):
    def add_to_collection(self, col, item):
        number = item['number']
        issue = col.find_one({'number': number})
        if not issue:
            col.insert(item)
        elif issue['modified_at'] != item['modified_at']:
            history_item = {
                'responsible': issue['responsible'],
                'state': issue['state'],
                'dev_owner': issue['dev_owner'],
                'modified_at': issue['modified_at']
            }
            history = issue.get('history', [])
            history.append(history_item)
            item['history'] = history
            col.update({'number': number}, item)

    def process_item(self, item, spider):
        issue = dict(item)
        self.add_to_collection(issues, issue)
        return item
