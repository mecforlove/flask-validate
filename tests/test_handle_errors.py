from flask import request, jsonify
from flask_validate import validate, Input, Validator
from wtforms.validators import DataRequired

from ._base import TestBase


class ArgsInput(Input):
    args = {'name': [DataRequired('name is required.')]}


class WithHandleErrorsArgsInput(ArgsInput):
    def handle_errors(self, e):
        return jsonify(dict(errors=e.errors)), 400


def handle_errors(e):
    return jsonify(e.errors), 400


class TestHandleErrors(TestBase):
    def test_app_handle_errors(self):
        validator = Validator(handle_errors=handle_errors)
        validator.init_app(self.app)

        @self.app.route('/who')
        @validate(ArgsInput)
        def who():
            return request.args.get('name')

        with self.app.test_client() as client:
            rv = client.get('/who')
            self.assertEqual(400, rv.status_code)
            self.assertEqual({
                'query_string': {
                    'name': ['name is required.']
                }
            }, rv.json)

    def test_input_handle_errors(self):
        @self.app.route('/who')
        @validate(WithHandleErrorsArgsInput)
        def who():
            return request.args.get('name')

        with self.app.test_client() as client:
            rv = client.get('/who')
            self.assertEqual(400, rv.status_code)
            self.assertEqual({
                'errors': {
                    'query_string': {
                        'name': ['name is required.']
                    }
                }
            }, rv.json)

    def test_input_cover_app_handler(self):
        validator = Validator(app=self.app, handle_errors=handle_errors)

        @self.app.route('/who')
        @validate(WithHandleErrorsArgsInput)
        def who():
            return request.args.get('name')

        with self.app.test_client() as client:
            rv = client.get('/who')
            self.assertEqual(400, rv.status_code)
            self.assertEqual({
                'errors': {
                    'query_string': {
                        'name': ['name is required.']
                    }
                }
            }, rv.json)

    def test_valid_input(self):
        @self.app.route('/who')
        @validate(WithHandleErrorsArgsInput)
        def who():
            return request.args.get('name')

        with self.app.test_client() as client:
            rv = client.get('/who?name=mec')
            self.assertEqual('mec', rv.data)
