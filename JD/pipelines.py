# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymongo
from scrapy.item import Item
from JD import settings


# class MongoPipeline(object):
    # # db_uri = "mongodb://127.0.0.1:27017/"
    # # db_name = 'test'
    #
    #
    # def open_spider(self, spider):
    #     self.client = MongoClient('127.0.0.1', 27017)
    #     self.db = self.client['test']
    #
    # def process_item(self, item, spider):
    #     collection = self.client['test']['jd']
    #     data = dict(item)
    #     collection.insert(data)
    #     print("****************")
    #     return item
    #
    # def close_spider(self, spider):
    #     self.client.close()




