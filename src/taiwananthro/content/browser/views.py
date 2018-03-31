# -*- coding: utf-8 -*-
from taiwananthro.content import _
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone import api
from Products.CMFPlone.utils import safe_unicode
import json
from plone.namedfile.field import NamedBlobImage
from plone.protect.interfaces import IDisableCSRFProtection
from zope.interface import alsoProvides
from plone.app.textfield.value import RichTextValue
import base64
import os
import urllib2
from plone import namedfile
import datetime
import time


class CreateNews(BrowserView):
    def __call__(self):
        request = self.request
        alsoProvides(request, IDisableCSRFProtection)
        portal = api.portal.get()
        js_data = request.get('data')
        data = json.loads(js_data)

        content = data['content']
        title = data['title']
        date = data['date']
        category = data['category'].encode('utf-8')
        img_src = data['img_src']

        if category == '學會新聞':
            en_catrgory = 'institute_news'
        elif category == '人類學界相關新聞':
            en_catrgory = 'anthropology_news'
        elif category == '活動':
            en_catrgory = 'event'
        elif category == '演講':
            en_catrgory = 'speech'
        elif category == '獎助學金':
            en_catrgory = 'reward'
        elif category == '徵人啟事':
            en_catrgory = 'recruitment_notice'
        elif category == '人類學相關學術刊物當期目錄':
            en_catrgory = 'anthropology_category'
        elif category == '國科會通過之人類學門計畫等	':
            en_catrgory = 'anthropology_plan'
        elif category == '相關學術公共政策':
            en_catrgory = 'policy'
        img_res = urllib2.urlopen(img_src)
        image = img_res.read()
        news = api.content.create(
            type='News',
            container=portal['news'][en_catrgory],
            title=title,
            category=en_catrgory,
            image=namedfile.NamedBlobImage(data=image, filename=unicode('pic.jpg')),
            richtext=RichTextValue(content),
        )
        news.setEffectiveDate(date)

class CreateDisseration(BrowserView):
    def __call__(self):
        request = self.request
        alsoProvides(request, IDisableCSRFProtection)
        portal = api.portal.get()
        js_data = request.get('data')
        data = json.loads(js_data)
        content = data['content']
        author = data['author']
        subject = data['subject']
        keyword = data['keyword']
        title = data['title']
        
        Disseration = api.content.create(
            type='Disseration',
            container=portal['annual_meeting']['2015'],
            title=title,
            author=author,
            keyword=keyword,
            content=RichTextValue(content),
        )
        Disseration.setSubject(subject)


class AnthroReportView(BrowserView):
    template = ViewPageTemplateFile('template/anthor_report_view.pt')
    def __call__(self):
        current = api.user.get_current()
        user_paid = current.getProperty('user_paid')
        request = self.request
        context = self.context
        alsoProvides(request, IDisableCSRFProtection)
        
        if user_paid:
            self.paid = True
        else:
            effective_timestamp = context.effective_date.timeTime()
            now_timestamp = time.time()
            if now_timestamp >= effective_timestamp + 518400:
                self.paid = True
            else:
                self.paid  = False
        return self.template()


class Cover(BrowserView):
    template = ViewPageTemplateFile('template/cover.pt')
    def __call__(self):
        request = self.request
        portal = api.portal.get()
        self.img_brain = api.content.find(context=portal['banner'],portal_type='Image'
            ,sort_on='created',sort_limit=4,sort_order="reverse")
        self.news_brain = api.content.find(context=portal['news'],portal_type="News"
            ,sort_on="created",sort_limit=6,sort_order="reverse")
        self.annual_meeting_brain = api.content.find(context=portal['annual_meeting'],portal_type="Folder"
            ,sort_on="created",sort_limit=1,sort_order="reverse")[0]
        self.research_publish_brain = api.content.find(context=portal['research_publish'],portal_type="AnthroReport"
            ,sort_on="created",sort_order="reverse",sort_limit=1)[0]

        return self.template()


class NewsView(BrowserView):
    template = ViewPageTemplateFile('template/news_view.pt')
    def __call__(self):
        context = self.context
        self.creation_date = context.creation_date.strftime('%Y年%m月%d日')
        self.title = context.title
        self.richtext = context.richtext.raw
        
        return self.template()