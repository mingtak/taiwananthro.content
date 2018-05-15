# -*- coding: utf-8 -*-
from plone.app.layout.viewlets import common as base
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone import api


class CoverSlider(base.ViewletBase):
    """  """
    def update(self):
        portal = api.portal.get()
        self.slider = portal['cover_slider'].listFolderContents()
