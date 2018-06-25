# coding: utf-8
from wtforms.validators import AnyOf
from werkzeug.datastructures import MultiDict
from flask_validate import Input

from ._base import TestBase


class HeadersInput(Input):
    headers = {'token': [AnyOf(['mecforlove'], message='token is required.')]}


class TestHeaders(TestBase):
    def test_valid_headers(self):
        valid_headers = MultiDict([('token', 'mecforlove')])
        with self.app.test_request_context(headers=valid_headers):
            self.assertTrue(HeadersInput().validate())

    def test_invalid_headers(self):
        invalid_headers = MultiDict([('token', 'mecforhate')])
        with self.app.test_request_context(headers=invalid_headers):
            self.assertFalse(HeadersInput().validate())

    def test_error_msg(self):
        invalid_headers = MultiDict([('token', 'mecforhate')])
        with self.app.test_request_context(headers=invalid_headers):
            input = HeadersInput()
            input.validate()
            self.assertEqual({
                'token': ['token is required.']
            }, input.errors['headers'])
