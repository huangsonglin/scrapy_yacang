# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import csv

class YachangPipeline(object):

    def __init__(self):
        self.file = open('name.csv', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        writer = csv.writer(self.file)
        writer.writerow(['拍场名', "拍场链接", '拍品数量', '拍卖公司', '拍卖城市', '拍卖专场类型', '拍卖时间', '拍卖状态',
                         '预展时间', '预展地点', '拍卖'])
        writer.writerow((item['name'], item['url'], item['lot_num'], item['aution_company'],
                         item['auction_city'], item['auction_classfy'], item['auction_time'], item['auction_status'],
                         item['preview_auction_time'], item['preview_auction_loction'],
                         item['official_auction_time'], item['official_auction_loction'],
                         item['lotImformation']))
        return item

    def spider_closed(self, spider):
        self.file.close()