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
            item = RepositoryItem()
            item['name'] =  course.xpath('.//h3/a/text()').re_first('[^\w]*(\w+)')
            item['update_time'] = course.xpath('.//relative-time/@datetime').extract_first()
            course_url = response.urljoin(course.xpath('.//h3/a/@href').extract_first())
            request = scrapy.Request(course_url, callback=self.parse_details)
            request.meta['item'] = item
            yield request
    
    def parse_details(self, response):
        item = response.meta['item']
        item['commits'] = response.css('li.commits span::text').extract_first()
        item['branches'] = response.xpath('//svg[@class="octicon octicon-git-branch"]/span/text()').extract_first()
        item['releases'] = response.xpath('//svg[@class="octicon octicon-git-tag"]/span/text()').extract_first() 
        yield item

        
