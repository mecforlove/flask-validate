# coding: utf-8
import unittest

from flask import Flask


class TestBase(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)