# -*- coding: utf-8 -*-
from plone import api
from taiwananthro.content import _
from zope.globalrequest import getRequest
from plone.app.textfield.value import RichTextValue


def replaceRichText(obj, attrStr):
    try:
        value = getattr(obj, attrStr, None).raw
        while 1:
            if '../resolveuid' in value:
                value = value.replace('../resolveuid', 'resolveuid')
            else:
                setattr(obj, attrStr, RichTextValue(value))
                break
    except:pass



def updateRichText(obj, event):

    replaceRichText(obj, 'text')
    replaceRichText(obj, 'abstract')
    replaceRichText(obj, 'metaData')
    replaceRichText(obj, 'richtext')
    replaceRichText(obj, 'content')


def moveImageToPubImage(obj, event):
    """
    Move Image Object to pub_image folder
    """
    portal = api.portal.get()

    if obj.getParentNode() not in (portal['pub_image'], portal['cover_slider']):
        api.content.move(source=obj, target=portal['pub_image'], safe_id=True)


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
