#! /urs/bin/env python3
# -*- coding:utf-8 -*-
import scrapy

class ShiyanlouGithubSpider(scrapy.Spider):

    name = 'github-repositories'
    @property
    def start_urls(self):
        url_tmpl = 'https://github.com/shiyanlou?page={}&tab=repositories'
        print(url_tmpl.format(i) for i in range(1, 5))
        return (url_tmpl.format(i) for i in range(1, 5))

    def parse(self, response):
        for repository in response.css('li.col-12'):
            yield{
                'name': repository.xpath('.//h3/a/text()').re_first('[^\w]*(\w+)'),
                'updated_time': repository.xpath('.//relative-time/@datetime').extract_first()
        }
