# -*- coding: utf-8 -*-
import urllib2
from bs4 import BeautifulSoup
import requests
import json


class get_new(object):
    def __init__(self, url):
        self.res = self.response(url)
        self.NewsList= self.getNewsList(self.res)
        
    def response(self, url):
        try:
            response = urllib2.urlopen(url.encode('utf-8'), timeout=2)
            return response
        except:
            print('抓取失敗'+url)
        else:
            print('抓取成功')

    def getNewsList(self, res):
        res = BeautifulSoup(res, 'lxml')
        newsList = res.select('#block-system-main')[0].find_all('div',{'class':'views-row'})
        hrefList = []
        for news in newsList:
            img_src = news.find('img')['src']
            # filetype = img_src.split('.')[-1]
            # img_res = urllib2.urlopen(img_src)
            # img = img_res.read()0..0
            # filename = 'img%s.%s' %(count, filetype)
            # pic_out = file(filename, 'w')
            # pic_out.write(img)
            # pic_out.close()
            # count += 1

            href = news.select('.post-title')[0].find('a')['href']
            url = 'http://www.taiwananthro.org.tw%s' % href

            res = urllib2.urlopen(url)
            res = BeautifulSoup(res, 'lxml')
            
            title = res.select('#content-header')[0].find('h1').text
            date = res.select('.date')[0].text.strip()
            category = res.select('.field-name-field-taxonomy-news')[0].select('.field-item.even')[0].find('a').text

            content = res.select('.field-name-body')[0].find_all('p')            
            content_str = ''

            for item in content:
                if not item.find('img'):
                    content_str += item.text + '<br>'
            data = {
                'title': title,
                'date': date,
                'category': category,
                'content': content_str,
                'img_src': img_src
            }
            js_data = json.dumps(data)
            requests.post('http://localhost:6051/taiwananthro/create_news', 
                          data={'data':js_data}, auth=('admin','123456'))

if __name__ == '__main__':
    
    news = get_new('http://www.taiwananthro.org.tw/news?page=15')
