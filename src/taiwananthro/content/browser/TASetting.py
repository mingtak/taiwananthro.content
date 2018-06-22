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
    footer = schema.Text(
        title=_(u"Footer Setting(HTML)"),
        required=False,
    )


class TASettingControlPanelForm(RegistryEditForm):
    form.extends(RegistryEditForm)
    schema = ITASetting

TASettingControlPanelView = layout.wrap_form(TASettingControlPanelForm, ControlPanelFormWrapper)
TASettingControlPanelView.label = _(u"Taiwan Anthropology Setting")
