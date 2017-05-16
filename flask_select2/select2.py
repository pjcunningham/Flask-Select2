# coding: utf-8
__author__ = 'Paul Cunningham'
__copyright = 'Copyright 2017, Paul Cunningham'

__all__ = ('Select2', )

from flask import Blueprint, request, abort, Response, json, current_app
from flask.views import MethodView


class Error(Exception):
    """Base class for exceptions in this module."""
    pass


class LoaderError(Error):
    def __init__(self, message):
        self.message = message


class Select2View(MethodView):

    def get(self):
        name = request.args.get('name')
        query = request.args.get('query')
        offset = request.args.get('offset', type=int)
        limit = request.args.get('limit', 10, type=int)
        _select = current_app.extensions.get('select2')

        if not _select:
            abort(404)

        _loader = _select.get_loader(name)

        if not _loader:
            abort(404)

        data = [_loader.format(m) for m in _loader.get_list(query, offset, limit)]
        return Response(json.dumps(data), mimetype='application/json')


class Select2(object):
    def __init__(self, app=None):

        self.app = None
        self.loaders = {}

        if app:
            self.app = app
            self.init_app(app)

    def init_app(self, app):
        app.config.setdefault('FLASK_SELECT2_RULE', '/ajax/lookup/')
        app.config.setdefault('FLASK_SELECT2_VIEW', 'ajax')
        self.register_blueprint(app)
        app.extensions['select2'] = self

    def register_blueprint(self, app):
        _module = Blueprint('select2', __name__, template_folder='templates', static_folder='static', static_url_path='/static/select2')
        _module.add_url_rule(app.config['FLASK_SELECT2_RULE'], view_func=Select2View.as_view(app.config['FLASK_SELECT2_VIEW']))
        app.register_blueprint(_module)
        return _module

    def add_loader(self, loader):
        if not loader.name in self.loaders:
            self.loaders[loader.name] = loader
        else:
            raise LoaderError(message='Call to add_loader with name : "{name}" already exists'.format(name=loader.name))

    def get_loader(self, name):
        _loader = self.loaders.get(name)
        if not _loader:
            raise LoaderError(message='Call to get_loader with name : "{name}" not found'.format(name=name))
        return _loader



