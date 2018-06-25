from flask_validate import Input
from flask_validate.validators import JsonSchema

from ._base import TestBase

schema = {'type': 'object', 'properties': {'name': {'type': 'string'}}}


class JsonInput(Input):
    json = [JsonSchema(schema)]


class TestJson(TestBase):
    def test_valid_json(self):
        with self.app.test_request_context(
                method='POST',
                data='{"name": "mec"}',
                content_type='application/json'):
            self.assertTrue(JsonInput().validate())

    def test_invalid_json(self):
        with self.app.test_request_context(
                method='POST',
                data='{"name": false}',
                content_type='application/json'):
            self.assertFalse(JsonInput().validate())

    def test_error_msg(self):
        with self.app.test_request_context(
                method='POST',
                data='{"name": false}',
                content_type='application/json'):
            input = JsonInput()
            input.validate()
            self.assertEqual({
                '_jsonschema': ["False is not of type 'string'"]
            }, input.errors['json'])
