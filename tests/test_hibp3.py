#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `hibp3` package."""


import unittest

from hibp3 import hibp3


class TestHibp3(unittest.TestCase):
    """Tests for `hibp3` package."""
    def hibptester(self):
        """Tests for hibp API requests"""
        valid = h.Checkemail("test@example.com")
        valid.fetch()
        valid.status()
    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_000_something(self):
        """Test something."""
