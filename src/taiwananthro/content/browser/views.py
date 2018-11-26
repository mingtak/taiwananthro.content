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
import csv
import sys
import pickle
import random
reload(sys)
sys.setdefaultencoding('utf-8')


class TestDebug(BrowserView):
    def __call__(self):
        alsoProvides(self.request, IDisableCSRFProtection)
        import pdb; pdb.set_trace()


class ContactUsView(BrowserView):
    template = ViewPageTemplateFile('template/contact_us_view.pt')
    def __call__(self):
        request = self.request
        portal = api.portal.get()

        recipient = api.portal.get_registry_record('taiwananthro.content.browser.TASetting.ITASetting.email')
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('message')
        if name and email and phone and message:
            api.portal.send_email(
                recipient=recipient,
                sender=email,
                subject=u'經 臺灣人類學與民族學學會 網站寄來的郵件，由 %s 發出' % name,
                body="電話: %s\n訊息:%s" % (phone, message),
            )
            api.portal.send_email(
                recipient="andy@mingtak.com.tw",
                sender=email,
                subject=u'經 臺灣人類學與民族學學會 網站寄來的郵件，由 %s 發出' % name,
                body="電話: %s\n訊息:%s" % (phone, message),
            )
            api.portal.show_message(message=u'感謝您的寶貴意見，訊息已發送。', request=request)
            request.response.redirect('%s/about_us/contact_us' % portal.absolute_url())
            return
        return self.template()


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


class AnthroArticleView(BrowserView):

    template = ViewPageTemplateFile('template/anthor_article_view.pt')

    def canSee(self):
        request = self.request
        context = self.context

        now = datetime.date.today()
        if now >= context.openDate:
            return True

        if api.user.is_anonymous():
            return False

        roles = api.user.get_roles()
        if 'Manager' in roles or 'Site Administrator' in roles:
            return True

        current = api.user.get_current()
        try:
            paid = current.getProperty('paid')
            event_member = current.getProperty('event_member')
        except:
            paid = None
            evetn_member = None

        if paid or event_member:
            return True
        else:
            return False


    def __call__(self):

        return self.template()


class AnthroReportView(AnthroArticleView):
    template = ViewPageTemplateFile('template/anthor_report_view.pt')

    # 歷期視界直接開放
    def is02(self):
        return self.context.getParentNode().id == '02'

    def getGroups(self):
        context = self.context

        children = context.getChildNodes()
        groups = []
        for item in children:
            if item.group not in groups:
                groups.append(item.group)

        return groups


class Cover(BrowserView):
    template = ViewPageTemplateFile('template/cover.pt')
    def __call__(self):
        request = self.request
        portal = api.portal.get()
        #self.slider = portal['cover_slider'].listFolderContents()
        self.news_brain = api.content.find(context=portal['news'],portal_type="News"
            ,sort_on="effective",sort_limit=6,sort_order="reverse")[0:6]
        self.annual_meeting = portal['annual_meeting']['annual_01']['current']
        self.research_publish = portal['anthropology_publish']['01']['current']

        return self.template()


class NewsView(BrowserView):
    template = ViewPageTemplateFile('template/news_view.pt')
    def __call__(self):
        context = self.context
        self.creation_date = context.creation_date.strftime('%Y年%m月%d日')
        self.title = context.title
        self.richtext = context.richtext.raw
        
        return self.template()


class CreateUser(BrowserView):
    def __call__(self):
        request = self.request
        portal = api.portal.get()
        alsoProvides(request, IDisableCSRFProtection)
        file = open('/home/henryc/taiwananthro.csv', 'r')
        csv_data = csv.reader(file)
        for data in csv_data:
            try:
                fullname = data[0]
                email = data[1]
                gender = data[2]
                birthday = data[3]
                education = data[4]
                job = data[5]
                registered_residence = data[6]
                cellphone = data[7]
                address = data[8]
                paid = data[9]
                event_member = data[10]
                if birthday:
                    year = birthday.split('/')[0]
                    month = birthday.split('/')[1]
                    day = birthday.split('/')[2]
                    year = int(year) + 1911
                    birthday = '%d-%s-%s' %(year, month, day)
                    birthday = datetime.datetime.strptime(birthday, '%Y-%m-%d')
                if paid == '已繳':
                    is_paid = True
                elif paid == '未繳':
                    is_paid = False
                if event_member == '是':
                    is_event_member = True
                elif event_member == '否':
                    is_event_member = False

                properties = dict(
                    fullname=fullname,
                    gender=gender,
                    birthday=birthday,
                    education=education,
                    job=job,
                    registered_residence=registered_residence,
                    cellphone=cellphone,
                    address=address,
                    paid=is_paid,
                    event_member=is_event_member
                )
                user = api.user.create(
                    email=email,
                    password='tA#$iW&9n',
                    properties=properties,
                )
            except Exception as e:
                print e.message
                print '%s 建立失敗' %fullname


class UserProfile(BrowserView):
    template = ViewPageTemplateFile('template/user_profile.pt')
    def __call__(self):
        abs_url = api.portal.get().absolute_url()
        request = self.request
        if api.user.is_anonymous():
            request.response.redirect('%s/login' %abs_url)
            return 
        current = api.user.get_current()

        self.fullname = current.getProperty('fullname')
        self.gender = current.getProperty('gender')
        birthday = current.getProperty('birthday')
        self.education = current.getProperty('education')
        self.job = current.getProperty('job')
        self.registered_residence = current.getProperty('registered_residence')
        self.cellphone = current.getProperty('cellphone')
        self.address = current.getProperty('address')
        paid = current.getProperty('paid')
        event_member = current.getProperty('event_member')
        self.birthday = birthday.strftime('%Y-%m-%d') if birthday else ''
        self.is_paid = '已繳' if paid else '未繳'
        self.is_event_member = '是' if paid else '否'
        self.email = current.getProperty('email')

        return self.template()


class UpdateUserProfile(BrowserView):
    def __call__(self):
        request = self.request
        abs_url = api.portal.get().absolute_url()
        if api.user.is_anonymous():
            request.response.redirect('%s/login' %abs_url)
            return 
        cellphone = request.get('cellphone', '')
        gender = request.get('gender', '')
        registered_residence = request.get('registered_residence', '')
        job = request.get('job', '')
        birthday = request.get('birthday', '')
        address = request.get('address', '')
        education = request.get('education', '')
        try:
            birthday_check = datetime.datetime.strptime(birthday, '%Y-%m-%d') if birthday else ''
	except:
	    request.response.redirect('%s/user_profile' %abs_url)
            api.portal.show_message('日期格式有誤,Ex:西元年-月-日', self.request, 'error')
	    return 
        current = api.user.get_current()
        current.setMemberProperties(mapping={
                                            'gender': gender,
                                            'registered_residence': registered_residence,
                                            'job': job,
                                            'cellphone': cellphone,
                                            'birthday': birthday_check,
                                            'address': address,
                                            'education': education,
                                        })
        abs_url = api.portal.get().absolute_url()
        request.response.redirect('%s/user_profile' %abs_url)


class ExportUsers(BrowserView):

    def __call__(self):
        request = self.request
        alsoProvides(request, IDisableCSRFProtection)

        users = api.user.get_users()
        userList = []
        for current in users:
            item = {}
            item['fullname'] = current.getProperty('fullname')
            item['gender'] = current.getProperty('gender')
            item['birthday'] = current.getProperty('birthday')
            item['education'] = current.getProperty('education')
            item['job'] = current.getProperty('job')
            item['registered_residence'] = current.getProperty('registered_residence')
            item['cellphone'] = current.getProperty('cellphone')
            item['address'] = current.getProperty('address')
            item['paid'] = current.getProperty('paid')
            item['event_member'] = current.getProperty('event_member')
            item['birthday'] = current.getProperty('birthday')
            item['email'] = current.getProperty('email')

            userList.append(item)
            api.user.delete(user=current)

        import pdb; pdb.set_trace()
        with open('/tmp/TAUserList', 'wb') as file:
            pickle.dump(userList, file)


class ImportUsers(BrowserView):

    def __call__(self):
        request = self.request
        alsoProvides(request, IDisableCSRFProtection)

        with open('/tmp/TAUserList') as file:
            users = pickle.load(file)

        for item in users:
            data = {}
            for k,v in item.items():
                data[k] = v
                if k == 'fullname':
                    print v

            user = api.user.create(
                username = 'u%s' % random.randint(10000000,99999999),
                password='tA#$iW&9n',
                properties=data,
            )


class DeleteUser(BrowserView):
    def __call__(self):
        request = self.request
        alsoProvides(request, IDisableCSRFProtection)

        users = api.user.get_users()
        for user in users:
            print user.getProperty('fullname')
            api.user.delete(user=user)
        return
