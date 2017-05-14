# coding: utf-8
__author__ = 'Paul Cunningham'
__copyright = 'Copyright 2017, Paul Cunningham'

from wtforms import fields
from flask_select2._compat import text_type, as_unicode
from . import widgets as select2_widgets


class Select2Field(fields.SelectField):
    """
        `Select2 <https://github.com/ivaynberg/select2>`_ styled select widget.

        You must include select2.js, form-x.x.x.js and select2 stylesheet for it to
        work.
    """
    widget = select2_widgets.Select2Widget()

    def __init__(self, label=None, validators=None, coerce=text_type,
                 choices=None, allow_blank=False, blank_text=None, **kwargs):
        super(Select2Field, self).__init__(
            label, validators, coerce, choices, **kwargs
        )
        self.allow_blank = allow_blank
        self.blank_text = blank_text or ' '

    def iter_choices(self):
        if self.allow_blank:
            yield (u'__None', self.blank_text, self.data is None)

        for value, label in self.choices:
            yield (value, label, self.coerce(value) == self.data)

    def process_data(self, value):
        if value is None:
            self.data = None
        else:
            try:
                self.data = self.coerce(value)
            except (ValueError, TypeError):
                self.data = None

    def process_formdata(self, valuelist):
        if valuelist:
            if valuelist[0] == '__None':
                self.data = None
            else:
                try:
                    self.data = self.coerce(valuelist[0])
                except ValueError:
                    raise ValueError(self.gettext(u'Invalid Choice: could not coerce'))

    def pre_validate(self, form):
        if self.allow_blank and self.data is None:
            return

        super(Select2Field, self).pre_validate(form)


class Select2TagsField(fields.StringField):
    """`Select2 <http://ivaynberg.github.com/select2/#tags>`_ styled text field.
    You must include select2.js, form-x.x.x.js and select2 stylesheet for it to work.
    """
    widget = select2_widgets.Select2TagsWidget()

    def __init__(self, label=None, validators=None, save_as_list=False, coerce=text_type, **kwargs):
        """Initialization

        :param save_as_list:
            If `True` then populate ``obj`` using list else string
        """
        self.save_as_list = save_as_list
        self.coerce = coerce

        super(Select2TagsField, self).__init__(label, validators, **kwargs)

    def process_formdata(self, valuelist):
        if valuelist:
            if self.save_as_list:
                self.data = [self.coerce(v.strip()) for v in valuelist[0].split(',') if v.strip()]
            else:
                self.data = self.coerce(valuelist[0])

    def _value(self):
        if isinstance(self.data, (list, tuple)):
            return u','.join(as_unicode(v) for v in self.data)
        elif self.data:
            return as_unicode(self.data)
        else:
            return u''
