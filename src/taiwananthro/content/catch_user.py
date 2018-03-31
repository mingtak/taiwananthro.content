# -*- coding: utf-8 -*-
import urllib2
from bs4 import BeautifulSoup
import requests
import json

def login():
    headers = {
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding':'gzip, deflate',
        'Accept-Language':'zh-TW,zh;q=0.8,en-US;q=0.6,en;q=0.4',
        'Cache-Control':'max-age=0',
        'Connection':'keep-alive',
        'Cookie':'Drupal.tableDrag.showWeight=0; __utmt=1; has_js=1; __utma=104179103.1164625419.1522200719.1522203029.1522391667.3; __utmb=104179103.3.10.1522391667; __utmc=104179103; __utmz=104179103.1522200719.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); SESS5f6a719c762e7aa86863dd2233f6631e=ocaWp9x6fuFHxZEKqxSJrOu5CCEQ0AUKF0eHQtEJ4Gk',
        'Host':'www.taiwananthro.org.tw',
        'If-None-Match':"1522388764-1",
        'Referer':'http://www.taiwananthro.org.tw/user/login?destination=front',
        'Upgrade-Insecure-Requests':'1',
        'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/59.0.3071.109 Chrome/59.0.3071.109 Safari/537.36',
    }
    url = 'http://www.taiwananthro.org.tw/user/login?destination=front'
    data = {
        'name':'tafea',
        'pass':'1qazse4',
        'form_build_id':'form-FjDGgpQGGVqkKFFYXLVfffSuo15lmG3yYKMvF9buHvQ',
        'form_id':'user_login',
        'op':'%E7%99%BB%E5%85%A5',
    }
    rs = requests.session()
    rs.post(url, data=data)
    response = rs.get('http://www.taiwananthro.org.tw/admin/structure/views/ajax/preview/admin_content/default?title=&type=member&promote=All&status=All&uid=&page=1')
    data = response.json()[1]['data']
    soup = BeautifulSoup(data, 'lxml')

    td_list = soup.find_all('td',{'class':'views-field views-field-edit-node'})
    for item in td_list:
        href = 'http://www.taiwananthro.org.tw%s' %item.findChild().attrs['href']
        response2 = rs.get(href)
        soup2 = BeautifulSoup(response2.text, 'lxml')
        pass_date = soup2.select('#edit-field-approval-und-0-value-datepicker-popup-0')[0].attrsp['value']
        name = soup2.select('#edit-title')[0].attrs['value']
        role = soup2.select('#edit-field-identity-und-select')[0].findChild().attr['value']
        job = soup2.select('#edit-field-organization-und-0-value')[0].attrs['value']
        img_src = soup2.select('.fi;e')[0].findChildren()[1].attrs['href']
        officephone = soup2.select('#edit-field-phone-office-und-0-value')[0].attrs['vlaue']
        mobilephone = soup2.select('#edit-field-phone-mobile-und-0-value')[0].attrs['vlaue']
        district = soup2.select('#edit-field-county-und-select')[0].attrs['value']
        area = soup2.select('#edit-field-area-und-select')[0].attrs['value']
        code = soup2.select('#edit-field-zipcode-und-0-value')[0].attrs['value']
        address = soup2.select('#edit-field-address-und-0-value')[0].attrs['value']
        email = soup2.select('#edit-field-email-und-0-email')[0].attrs['value']
        education = soup2.select('#edit-field-highest-education-und-0-value')[0].text
        experience = soup2.select('#edit-field-experience-und-0-value')[0].attrs['value'].text
        recommend1 = soup2.select('#edit-field-recommend-1-und-0-value')[0].attrs['value']
        recommend2 = soup2.select('#edit-field-recommend-2-und-0-value')[0].attrs['value']

login()