from PyIRC.irc.message import (
    extract_prefix, InvalidMessageException, validate_message)

import unittest


class TestMessageValidation(unittest.TestCase):
    """Test message format validation functions."""

    def test_extract_prefix_valid_prefix(self):
        """Test that a valid prefix can be extracted from a message."""

        message = ":nickname COMMAND"

        prefix, content = extract_prefix(message)
        self.assertEquals(prefix, "nickname")

    def test_extract_prefix_no_prefix(self):
        """Test that if there is no prefix it works fine."""

        message = "COMMAND"

        prefix, content = extract_prefix(message)
        self.assertEquals(prefix, "")

    def test_extract_prefix_valid_servername_leading_letter(self):
        """
        Test that a valid servername with leading letter can be
        extracted.
        """

        message = ":hostname999-9 STUFF"

        prefix, content = extract_prefix(message)
        self.assertEquals(prefix, "hostname999-9")

    def test_extract_prefix_valid_servername_leading_digit(self):
        """
        Test that a valid servername with leading digit can be
        extracted.
        """

        message = ":1hostname999-9 STUFF"

        prefix, content = extract_prefix(message)
        self.assertEquals(prefix, "1hostname999-9")

    @unittest.skip("Not working yet")
    def test_extract_prefix_invalid_servername_trailing_hyphen(self):
        """
        Test that an invalid servername with trailing hyphen can't be
        extracted.
        """

        message = ":hostname999- STUFF"

        self.assertRaises(InvalidMessageException, extract_prefix, message)
