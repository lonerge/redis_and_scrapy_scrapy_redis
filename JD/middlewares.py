# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from selenium import webdriver
import time
from scrapy.http import HtmlResponse
# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter







class SeleniumWiddleware:

    def process_request(self, request, spider):
        url = request.url
        # 过滤url(一般的使用selenium会很慢, 所以只渲染必须渲染的url)
        if '过滤条件' in request.url:
            driver = webdriver.Chrome()
            driver.get(url=url)
            time.sleep(3)
            # 获取渲染之后的源码
            response = driver.page_source
            # 因为要返回的是response(定制中间件返回渲染之后的response给到爬虫里面的解析方法)
            driver.close()
            # 创建响应对象:
            res = HtmlResponse(url=url, body=response, encoding='utf-8', request=request)
            # 因为这里process_request只能返回三种值(None,request.response),所以不能用yield
            return res






class JdSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class JdDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        url = request.url
        # 过滤url(一般的使用selenium会很慢, 所以只渲染必须渲染的url)
        if '%5E5283_' in request.url:
            opt = webdriver.ChromeOptions()
            opt.add_argument('--headless')
            opt.add_argument('--gpu-disable')
            driver = webdriver.Chrome(chrome_options=opt)
            driver.get(url=url)
            time.sleep(1)
            driver.execute_script('scrollTo(0,20000)')
            time.sleep(2)
            # 获取渲染之后的源码
            response = driver.page_source
            # 因为要返回的是response(定制中间件返回渲染之后的response给到爬虫里面的解析方法)
            driver.close()
            # 创建响应对象:
            res = HtmlResponse(url=url, body=response, encoding='utf-8', request=request)
            # 因为这里process_request只能返回三种值(None,request.response),所以不能用yield
            return res

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
