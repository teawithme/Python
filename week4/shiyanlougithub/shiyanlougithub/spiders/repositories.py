# -*- coding: utf-8 -*-
import scrapy
from shiyanlougithub.items import RepositoryItem

class RepositoriesSpider(scrapy.Spider):
    name = 'repositories'
    #allowed_domains = ['github.com']
    @property
    def start_urls(self):
        url_tmpl = 'https://github.com/shiyanlou?page={}&tab=repositories'
        return (url_tmpl.format(i) for i in range(1, 5))

    def parse(self, response):
        for course in response.xpath('//li[contains(@class, "d-block")]'):
            item = RepositoryItem({
                'name': course.xpath('.//h3/a/text()').re_first('[^\w]*(\w+)'),
                'update_time': course.xpath('.//relative-time/@datetime').extract_first()
                })
            yield item
