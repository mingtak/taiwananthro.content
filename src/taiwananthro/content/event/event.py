# -*- coding: utf-8 -*-
from plone import api
from taiwananthro.content import _
from zope.globalrequest import getRequest


def toFolderContents(obj, event):
    """
    Return to Folder Contents
    """
    request = getRequest()
    folder = obj.getParentNode()
    if folder == None:
        try:
            folder = api.portal.get()
        except:
            return
    elif getattr(obj, 'portal_type', None) == 'Plone Site':
        folder = obj

    if request:
        request.response.redirect('%s/folder_contents' % folder.absolute_url())


def back_to_cover(event):
    request = getRequest()
    abs_url = api.portal.get().absolute_url()
    request.response.redirect(abs_url)


def moveObjectsToTop(obj, event):
    """
    Moves Items to the top of its folder
    """
    folder = obj.getParentNode()
    if folder != None and hasattr(folder, 'moveObjectsToTop'):
        folder.moveObjectsToTop(obj.id)
