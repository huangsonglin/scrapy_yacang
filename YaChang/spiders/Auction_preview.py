# -*- coding: utf-8 -*-
import scrapy
import re
from YaChang.items import YachangItem


class AuctionPreviewSpider(scrapy.Spider):
    name = 'Auction_preview'
    defult_url = 'https://auction.artron.net'
    # allowed_domains = ['www.artron.net']
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
        'Referer': 'https://auction.artron.net/preauction/',
        'Origin': 'https://auction.artron.net'}
    def start_requests(self):
        url = 'https://auction.artron.net/preauction/'
        yield scrapy.Request(url, headers=self.headers, callback=self.parse)

    def parse(self, response):
        nameList = response.xpath('//*[@class="name"]/a/@title').extract()
        urlList = response.xpath('//*[@class="name"]/a/@href').extract()
        lotList = response.xpath('//li[@class="sum"]/text()').extract()[1:]
        companyList = response.xpath('//*[@class="company"]/a/text()').extract()
        cityList = response.xpath('//li[@class="city"]/text()').extract()[1:]
        timeList = response.xpath('//li[@class="time"]/text()').extract()[1:]
        statusList = response.xpath('//li[@class="status"]/text()').extract()[1:]
        maxpage = response.xpath('//*[@class="sum"]/text()').extract()[-1]
        maxpage = ''.join(re.findall('\d', maxpage))
        for i in range(len(nameList)):
            item = YachangItem()
            item['name'] = nameList[i]
            item['url'] = self.defult_url + urlList[i]
            item['lot_num'] = lotList[i]
            item['aution_company'] = companyList[i]
            item['auction_city'] = cityList[i]
            item['auction_time'] = timeList[i]
            item['auction_status'] = statusList[i]
            # yield item
            detailurl = self.defult_url + urlList[i]
            yield scrapy.Request(url=detailurl, callback=self.parse_detail, meta={'item': item})

        next_page_url = response.xpath('//*[@class="page-next"]/@href').extract_first()
        current_page_url = response.xpath('//*[@class="page_cur"]/@href').extract_first()
        currentPage = response.xpath('//*[@class="page_cur"]/text()').extract_first()
        if int(currentPage) <= int(maxpage):
            next_page_url = self.defult_url + next_page_url
            yield scrapy.Request(next_page_url, callback=self.parse)


    def parse_detail(self, response):
        item = response.meta['item']
        timeList = response.xpath('//*[@class="infDetail"]//li/text()').extract()
        locList = response.xpath('//*[@class="infDetail"]//li/p/text()').extract()
        classfyList = response.xpath('//*[@class="specNote"]//h3/a/text()').extract()
        classfyUrlList = response.xpath('//*[@class="specNote"]//h3/a/@href').extract()
        item['preview_auction_time'] = timeList[0].strip()
        item['official_auction_time'] = timeList[-1].strip()
        item['preview_auction_loction'] = locList[0].strip()
        if len(locList) == 1:
            item['official_auction_loction'] = locList[0].strip()
        else:
            item['official_auction_loction'] = locList[1].strip()
        for i in range(len(classfyList)):
            item['auction_classfy'] = classfyList[i]
            ClassFyUrl = self.defult_url + classfyUrlList[i]
            yield scrapy.Request(url=ClassFyUrl, callback=self.parese_lot_detail, meta={"item": item})

    def parese_lot_detail(self, response):
        item = response.meta['item']
        ImgList = response.xpath('//*[@class="imgList specWorks clearfix"]/li').extract()
        NULL = ['<li style="text-align:center;font-size:14px;font-family:Microsoft Yahei;padding:40px 0;width:100%;">即将上传，敬请期待！</li>']
        if ImgList != NULL:
            maxpage = response.xpath('//*[@class="sum"]/text()').extract()[-1]
            maxpage = ''.join(re.findall('\d', maxpage))
            lotUrlList = response.xpath('//*[@class="imgList specWorks clearfix"]//h3/a/@href').extract()
            lotNameList = response.xpath('//*[@class="imgList specWorks clearfix"]//h3/a/text()').extract()
            lotPriceList = response.xpath('//*[@class="red"]/text()').extract()
            lotCityList = response.xpath(
                '//*[@class="imgList specWorks clearfix"]//ul[@class="dataItem"]/li[3]/text()').extract()
            LOT_INFORMATION = []
            for i in range(len(lotNameList)):
                lot_imfromation = {"name": lotNameList[i], "url": lotUrlList[i],
                                   "price": lotPriceList[i], "city": lotCityList[i]}
                LOT_INFORMATION.append(lot_imfromation)
            item['lotImformation'] = str(LOT_INFORMATION)
            yield item

            next_page_url = response.xpath('//*[@class="page-next"]/@href').extract_first()
            current_page_url = response.xpath('//*[@class="page_cur"]/@href').extract_first()
            currentPage = response.xpath('//*[@class="page_cur"]/text()').extract_first()
            if int(currentPage) <= int(maxpage):
                next_page_url = self.defult_url + next_page_url
                yield scrapy.Request(next_page_url, callback=self.parese_lot_detail, meta={"item":item})
        else:
            item['lotImformation'] = 'NULL'
            yield item






