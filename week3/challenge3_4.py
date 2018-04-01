#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import re
from datetime import datetime

def open_parser(filename):
    with open(filename) as logfile:
        #print(logfile.read())
        pattern = (r''
                   r'(\d+.\d+.\d+.\d+)\s-\s-\s'
                   r'\[(.+)\]\s'
                   r'"GET\s(.+)\s\w+/.+"\s'
                   r'(\d+)\s'
                   r'(\d*)\s'
                   r'"(.+)"\s'
                   r'"(.+)"'
                   )
        parsers = re.findall(pattern, logfile.read())
    return parsers

def main():
    logs = open_parser('nginx.log')

    ipct_dict = {}
    url404_dict = {}
    for log in logs:
        ip = log[0]
        date = log[1]
        ymd = datetime.strptime(date,'%d/%b/%Y:%H:%M:%S %z')
        ymd = datetime.strftime(ymd, '%Y-%m-%d')
        #print(ymd)
        url = log[2]
        status = log[3]
        #print(date.year)
        if ymd == '2017-01-11':
            if ipct_dict.get(ip) is None:
                ipct_dict[ip] = 1
            else:
                ipct_dict[ip] += 1
        if status == '404':
            if url404_dict.get(url) is None:
                url404_dict[url] = 1
            else:
                url404_dict[url] += 1

    ipct_list = sorted(ipct_dict.items(), key=lambda x: x[1], reverse=True)
    ip_dict = dict([(ipct_list[0])])
    #print(ip_dict)
    url_list = sorted(url404_dict.items(), key=lambda x: x[1], reverse=True)
    url_dict = dict([(url_list[0])])
    #print(url404_dict)

    return ip_dict, url_dict

if __name__ == '__main__':
    ip_dict, url_dict = main()
    print(ip_dict, url_dict)
    #main()
