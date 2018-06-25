# coding: utf-8
from functools import wraps

from flask import request, current_app
from werkzeug.datastructures import MultiDict
from wtforms.form import BaseForm
from wtforms.fields import Field


def validate(input_model):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            input = input_model()
            if hasattr(input, 'handle_errors'):
                current_app.errorhandler(ValidateError)(input.handle_errors)
            if input.validate():
                return func(*args, **kwargs)
            else:
                raise ValidateError(input.errors)

        return wrapper

    return decorator


class Validator(object):
    def __init__(self, app=None, handle_errors=None):
        self.handle_errors = handle_errors
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.app = app

        if callable(self.handle_errors):
            self.app.errorhandler(ValidateError)(self.handle_errors)


class Input(object):
    headers = {}
    args = {}
    form = {}
    json = []

    def __init__(self, req=None):
        if req is None:
            req = request
        self._request = req
        self.errors = {}

        fields = {}
        for name, validators in self.headers.items():
            fields[name] = Field(validators=validators)
        self._headers_form = BaseForm(fields)

        fields.clear()
        for name, validators in self.args.items():
            fields[name] = Field(validators=validators)
        self._args_form = BaseForm(fields)

        fields.clear()
        for name, validators in self.form.items():
            fields[name] = Field(validators=validators)
        self._form_form = BaseForm(fields)

        fields.clear()
        fields['_jsonschema'] = Field(validators=self.json)
        self._json_form = BaseForm(fields)

    def validate(self):
        success = True
        self._headers_form.process(self._request.headers)
        if not self._headers_form.validate():
            success = False
            self.errors['headers'] = self._headers_form.errors
        self._args_form.process(self._request.args)
        if not self._args_form.validate():
            success = False
            self.errors['query_string'] = self._args_form.errors
        self._form_form.process(self._request.form)
        if not self._form_form.validate():
            success = False
            self.errors['form'] = self._form_form.errors
        self._json_form.process(
            MultiDict(
                dict(_jsonschema=self._request.get_json(
                    force=True, silent=True))),
            coerse=False)
        if not self._json_form.validate():
            success = False
            self.errors['json'] = self._json_form.errors
        return success


class ValidateError(Exception):
    def __init__(self, errors, message=''):
        super(ValidateError, self).__init__(message)
        self.errors = errors
