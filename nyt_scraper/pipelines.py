from scrapy.exceptions import DropItem
from scrapy import log
import firebase_admin
from firebase_admin import credentials, firestore
import hashlib

cred = credentials.Certificate("service_acc_key.json")
firebase_admin.initialize_app(cred,
                              {'projectId': 'nyt-archives'})


def h11(w):
    return hashlib.md5(w.encode('utf-8')).hexdigest()[:9]


COLLECTION_NAME = 'headlines'
store = firestore.client()
collection_ref = store.collection(COLLECTION_NAME)
# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class HeadlinePipeline(object):
    def process_item(self, item, spider):
        doc_name = h11(item['headline'])
        doc_ref = collection_ref.document(doc_name)
        validated = True
        for data in item:
            if not data:
                validated = False
                raise DropItem('Missing {}'.format(data))
        if validated:
            doc_ref.set(dict(item))
            log.msg(f'{doc_name} added to Firestore collection!',
                    level=log.DEBUG, spider=spider)
        return item
