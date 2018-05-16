# -*- coding: utf-8 -*-
from plone.app.layout.viewlets import common as base
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone import api
from zope.component import queryUtility
from plone.i18n.normalizer.interfaces import IIDNormalizer


class HeaderTools(base.ViewletBase):
    """  """
    def update(self):
        self.portal = api.portal.get()
        self.isAnon = api.user.is_anonymous()
        self.isMana = 'Manager' in api.user.get_roles()

        normalizer = queryUtility(IIDNormalizer)
        permissions = []
        for permission, roles in getattr(self.view, '__ac_permissions__', tuple()):
            permissions.append(normalizer.normalize(permission))
        if 'none' in permissions or 'view' in permissions:
            self.isFrontend = True
        else:
            self.isFrontend = False
        if not self.isAnon:
            self.current = api.user.get_current()


class CoverSlider(base.ViewletBase):

    def update(self):
        portal = api.portal.get()
        self.slider = portal['cover_slider'].listFolderContents()
