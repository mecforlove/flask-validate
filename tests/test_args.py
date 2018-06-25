from wtforms.validators import DataRequired
from flask_validate import Input

from ._base import TestBase


class ArgsInput(Input):
    args = {'name': [DataRequired(message='name is required.')]}


class TestArgs(TestBase):
    def test_valid_args(self):
        with self.app.test_request_context(query_string='name=mec'):
            self.assertTrue(ArgsInput().validate())

    def test_invalid_args(self):
        with self.app.test_request_context():
            self.assertFalse(ArgsInput().validate())

    def test_error_msg(self):
        with self.app.test_request_context():
            input = ArgsInput()
            input.validate()
            self.assertEqual({
                'name': ['name is required.']
            }, input.errors['query_string'])
