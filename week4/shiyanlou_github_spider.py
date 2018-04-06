#! /urs/bin/env python3
# -*- coding:utf-8 -*-
import scrapy

class ShiyanlouGithubSpider(scrapy.Spider):

    name = 'github-repositories'

    def start_url(self):
        url_tmpl = 'https://github.com/shiyanlou?page={}&tab=repositories'
        return (url_tmpl.format(i) for i in range(1, 5))

    def parse(self, response):
        for repository in response.css('div.[d-inline-block mb-1']):
            yield{
                'name': repository.xpath('//h3/a/text()').extract_first(),
                'updated_time': repository.xpath(//relative-time/@datetime).extract_first()
        }
