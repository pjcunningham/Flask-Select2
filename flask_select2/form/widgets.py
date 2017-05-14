# coding: utf-8
__author__ = 'Paul Cunningham'
__copyright = 'Copyright 2017, Paul Cunningham'

from wtforms import widgets

__all__ = ['Select2Widget', 'Select2TagsWidget', ]


class Select2Widget(widgets.Select):
    """
    """
    def __call__(self, field, **kwargs):
        kwargs.setdefault('data-role', u'select2')

        allow_blank = getattr(field, 'allow_blank', False)
        if allow_blank and not self.multiple:
            kwargs['data-allow-blank'] = u'1'

        return super(Select2Widget, self).__call__(field, **kwargs)


class Select2TagsWidget(widgets.TextInput):
    """
    """
    def __call__(self, field, **kwargs):
        kwargs.setdefault('data-role', u'select2-tags')
        return super(Select2TagsWidget, self).__call__(field, **kwargs)