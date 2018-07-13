# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""
from taiwananthro.content import _
from zope import schema
from plone.supermodel import model
from zope.interface import Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from z3c.relationfield.schema import RelationList, RelationChoice
from plone.app.vocabularies.catalog import CatalogSource
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from plone.namedfile.field import NamedBlobImage,NamedBlobFile
from plone.app.textfield import RichText
from plone.dexterity.content import Container
from zope.interface import implementer


news_catagory = SimpleVocabulary(
    [SimpleTerm(value=u'institute_news', title=_(u'institute_news')),
     SimpleTerm(value=u'anthropology_news', title=_(u'anthropology_news')),
     SimpleTerm(value=u'event', title=_(u'event')),
     SimpleTerm(value=u'speech', title=_(u'speech')),
     SimpleTerm(value=u'reward', title=_(u'reward')),
     SimpleTerm(value=u'recruitment_notice', title=_(u'recruitment_notice')),
     SimpleTerm(value=u'anthropology_category', title=_(u'anthropology_category')),
     SimpleTerm(value=u'anthropology_plan', title=_(u'anthropology_plan')),
     SimpleTerm(value=u'policy', title=_(u'policy')),]
)
web_site = SimpleVocabulary(
    [
        SimpleTerm(value=u'domestic', title=_(u'domestic')),
        SimpleTerm(value=u'foreign', title=_(u'foreign')),
])
class ITaiwananthroContentLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


class INews(Interface):
    
    title = schema.TextLine(
        title=_(u'Title'),
        required=True,
    )

    category = schema.Choice(
        title=_(u'Category'),
        vocabulary=news_catagory,
        required=True,
    )

    image = NamedBlobImage(
        title=_(u"News Image."),
        required=False
    )

    richtext = RichText(
        title=_(u"Content Text"),
        required=True,
    )


class IDisseration(Interface):
    author = schema.TextLine(
        title=_(u'Author'),
        required=False
    )
    keyword = schema.TextLine(
        title=_(u"Key Word"),
        required=False
    )
    content = RichText(
        title=_(u"Content Text"),
        required=False,
    )


class IAnthroReport(Interface):
    title = schema.TextLine(
        title=_(u'Title'),
        required=True
    )

    description = schema.Text(
        title=_(u'Description'),
        required=False
    )

    cover_image = NamedBlobImage(
        title=_(u"Current Cover Image."),
        required=True
    )

    openDate = schema.Date(
        title=_(u"Full Text Open Date"),
        required=True
    )

    file = NamedBlobFile(
        title=_(u'Full File'),
        required=False
    )

@implementer(IAnthroReport)
class AnthroReport(Container):
    """
    """

class IAnthroArticle(Interface):
    title = schema.TextLine(
        title=_(u'Title'),
        required=True
    )

    openDate = schema.Date(
        title=_(u"Open Date"),
        required=True
    )

    group = schema.TextLine(
        title=_(u'Group'),
        required=False
    )

    pages = schema.TextLine(
        title=_(u'Pages'),
        required=True
    )

    authorName = schema.TextLine(
        title=_(u'Author Name'),
        required=True
    )

    metaData = RichText(
        title=_(u'Meta Data'),
        required=False
    )

    abstract = RichText(
        title= _(u"Abstract"),
        required=False
    )

    keyword = schema.TextLine(
        title=_(u"Keywords"),
        description=_(u"Split with common(,)"),
        required=False,
    )

    text = RichText(
        title= _(u"Full Text"),
        required=False
    )

    file = NamedBlobFile(
        title= _(u"Attach File"),
        required=False
    )


class IRelatedWebsite(Interface):
    title = schema.TextLine(
        title=_(u'Web Site'),
        required=False
    )
    url = schema.URI(
        title=_(u'Web Site URL'),
        required=False
    )
    choice = schema.Choice(
        title=_(u'domestic? foreign?'),
        vocabulary=web_site,
        required=False
    )
