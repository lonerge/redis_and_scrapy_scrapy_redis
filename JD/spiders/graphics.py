import scrapy
import json
from JD import items
import time
import re
from scrapy_redis.spiders import RedisSpider


class GraphicsSpider(RedisSpider):
    name = 'graphics'
    # allowed_domains = ['jd.com']
    # start_urls = ['https://list.jd.com/list.html?cat=670%2C677%2C679&cid3=679&cid2=677']
    redis_key = "start_JD"

    def __init__(self, *args, **kwargs):
        domain = kwargs.pop('domin', '')
        self.allowed_domains = list(filter(None, domain.split(',')))
        super(GraphicsSpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        # pass
        # 拿到所有显卡品牌节点
        brand_list = response.xpath('//ul[@class="J_valueList v-fixed"]//li')
        # print(len(brand_list))
        for brand in brand_list[:3]:
            item = dict()
            item['brand'] = brand.xpath('./a/@title').extract_first()
            # print(item)
            url = response.urljoin(brand.xpath('./a/@href').extract_first())
            # print(url)
            yield scrapy.Request(
                url=url, callback=self.parse_model, meta={'item': item}
            )

    def parse_model(self, response):
        item = response.meta['item']
        # 拿到所有的显卡类型节点
        model_list = response.xpath('//*[@id="J_selector"]/div[2]//ul[@class="J_valueList"]/li')
        for model in model_list[:3]:
            temp = dict()
            temp['brand'] = item['brand']
            temp["model"] = model.xpath('./a/text()').extract_first()
            url = response.urljoin(model.xpath('./a/@href').extract_first())
            # print(url)
            # print(item)
            yield scrapy.Request(
                url=url, callback=self.parse_graphics, meta={'item': temp}
            )

    def parse_graphics(self, response):
        item = response.meta['item']
        # time.sleep(2)
        # 找到所有的显卡商品节点
        graphics_list = response.xpath('//*[@id="J_goodsList"]/ul/li')
        print(len(graphics_list))
        for graphics in graphics_list:
            temp = dict()
            temp['brand'] = item['brand']
            temp["model"] = item["model"]
            temp["id"] = graphics.xpath('./@data-sku').extract_first()
            temp["name"] = graphics.xpath('./div/div[3]/a/em/text()').extract_first()
            temp["shop"] = graphics.xpath('./div/div[5]/span/a/text()').extract_first()
            # temp["assessment"] = graphics.xpath('./div/div[4]/strong/text()').extract_first()
            # temp["assessment"] = graphics.xpath('//*[@id=id]').extract_first()
            temp["price"] = graphics.xpath('./div/div[2]/strong/i/text()').extract_first()
            # print(temp)
            url = 'https://club.jd.com/comment/productCommentSummaries.action?referenceIds=' + temp["id"]
            yield scrapy.Request(
                url=url,
                callback=self.parse_assessment,
                meta={'item': temp}
            )

        url1 = 'https://search.jd.com/script/search_new.init.js?2021-12-23-18!'
        yield scrapy.Request(
            url=url1,
            callback=self.next_page
            # meta={'next': next_page}
        )

    def next_page(self, response):
        # 模拟翻页
        for i in range(1, 10):
            # next_page = re.search(r'pn-next disabled', response.text)
            # if next_page:
            #     break
            # else:
            url_2 = response.request.url.replace('&cid3=679', '') + '&page=' + str(2 * i + 1) + '&s=' + str(
                i * 60 + 1) + '&click=0'
            yield scrapy.Request(
                url=url_2,
                callback=self.parse_graphics)

    def parse_assessment(self, response):
        # 返回的响应是json字符串
        data = json.loads(response.text)
        item = response.meta['item']
        retu_item = items.JdItem()
        retu_item['brand'] = item['brand']
        retu_item['model'] = item['model']
        retu_item['name'] = item['name']
        retu_item['shop'] = item['shop']
        retu_item['price'] = item['price']
        retu_item['assessment'] = data["CommentsCount"][0]["CommentCountStr"]
        retu_item['good_assessment'] = data["CommentsCount"][0]["GoodCountStr"]
        print(retu_item)
        # yield retu_item

# https://list.jd.com/list.html?cat=670%2C677%2C679&ev=exbrand_%E6%8A%80%E5%98%89%EF%BC%88GIGABYTE%EF%BC%89%5E5283_176433%5E&cid3=679
# https://list.jd.com/list.html?cat=670%2C677%2C679&ev=exbrand_%E6%8A%80%E5%98%89%EF%BC%88GIGABYTE%EF%BC%89%5E5283_176433%5E&page=3&s=61&click=0
# https://list.jd.com/list.html?cat=670%2C677%2C679&ev=exbrand_%E6%8A%80%E5%98%89%EF%BC%88GIGABYTE%EF%BC%89%5E5283_176433%5E&page=5&s=121&click=0
# https://list.jd.com/list.html?cat=670%2C677%2C679&ev=exbrand_%E5%8D%8E%E7%A1%95%EF%BC%88ASUS%EF%BC%89%5E5283_175352%5E&page=7&s=181&click=1