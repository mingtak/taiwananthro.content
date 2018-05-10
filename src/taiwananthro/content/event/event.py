# -*- coding: utf-8 -*-
from plone import api
from taiwananthro.content import _
from zope.globalrequest import getRequest


def back_to_cover(event):
    request = getRequest()
    abs_url = api.portal.get().absolute_url()
    request.response.redirect(abs_url)


def moveObjectsToTop(obj, event):
    """
    Moves Items to the top of its folder
    """
    folder = obj.getParentNode()
    if folder != None:
        folder.moveObjectsToTop(obj.id)
