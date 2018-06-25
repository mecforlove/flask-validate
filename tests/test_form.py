from wtforms.validators import DataRequired
from flask_validate import Input

from ._base import TestBase


class FormInputs(Input):
    form = {'name': [DataRequired(message='name is required.')]}


class TestForm(TestBase):
    def test_valid_form(self):
        with self.app.test_request_context(
                method='POST', data={'name': 'mec'}):
            self.assertTrue(FormInputs().validate())

    def test_invalid_form(self):
        with self.app.test_request_context(method='POST'):
            self.assertFalse(FormInputs().validate())

    def test_error_msg(self):
        with self.app.test_request_context(method='POST'):
            input = FormInputs()
            input.validate()
            self.assertEqual({
                'name': ['name is required.']
            }, input.errors['form'])
