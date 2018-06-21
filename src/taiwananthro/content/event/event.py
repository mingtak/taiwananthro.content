# -*- coding: utf-8 -*-
from plone import api
from taiwananthro.content import _
from zope.globalrequest import getRequest
from plone.app.textfield.value import RichTextValue


def replaceRichText(obj, attrStr):
    try:
        attr = getattr(obj, attrStr, None).text.raw
        while 1:
            if '../resolveuid' in text:
                text = text.replace('../resolveuid', 'resolveuid')
            else:
                obj.text = RichTextValue(text)
                break
    except:pass



def updateRichText(obj, event):
    # text
    try:
        text = obj.text.raw
        while 1:
            if '../resolveuid' in text:
                text = text.replace('../resolveuid', 'resolveuid')
            else:
                obj.text = RichTextValue(text)
                break
    except:pass

    # abstract
    try:
        abstract = obj.abstract.raw
        while 1:
            if '../resolveuid' in abstract:
                abstract = abstract.replace('../resolveuid', 'resolveuid')
            else:
                obj.abstract = RichTextValue(abstract)
                break
    except:pass

    # metaData
    try:
        metaData = obj.metaData.raw
        while 1:
            if '../resolveuid' in metaData:
                metaData = metaData.replace('../resolveuid', 'resolveuid')
            else:
                obj.metaData = RichTextValue(metaData)
                break
    except:pass


def moveImageToPubImage(obj, event):
    """
    Move Image Object to pub_image folder
    """
    portal = api.portal.get()
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
