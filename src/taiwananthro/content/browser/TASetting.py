# -*- coding: utf-8 -*-
from taiwananthro.content import _
from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper

from plone.z3cform import layout
from z3c.form import form
from plone.directives import form as Form
from zope import schema


class ITASetting(Form.Schema):

    """ Basic setting for taiwananthro """

    map = schema.Text(
        title=_(u"Google map embeded code"),
        required=False,
    )

    address1 = schema.Text(
        title=_(u"Address1"),
        required=False,
    )

    address2 = schema.Text(
        title=_(u"Address2"),
        required=False,
    )

    email = schema.TextLine(
        title=_(u"Email"),
        required=False,
    )

    footer = schema.Text(
        title=_(u"Footer Setting(HTML)"),
        required=False,
    )


class TASettingControlPanelForm(RegistryEditForm):
    form.extends(RegistryEditForm)
    schema = ITASetting

TASettingControlPanelView = layout.wrap_form(TASettingControlPanelForm, ControlPanelFormWrapper)
TASettingControlPanelView.label = _(u"Taiwan Anthropology Setting")
