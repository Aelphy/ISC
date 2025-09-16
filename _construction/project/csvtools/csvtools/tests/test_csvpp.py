import io
import sys
import unittest

from csvtools.csvtools.csvpp import print_row
from csvtools.csvtools.utils import InputError


class TestPrintRow(unittest.TestCase):
    def setUp(self):
        self.stream = io.StringIO()
        self.new_stdout = io.StringIO()
        self.new_stderr = io.StringIO()
        self.old_stdout = sys.stdout
        self.old_stderr = sys.stderr

        sys.stdout = self.new_stdout
        sys.stderr = self.new_stderr

    def tearDown(self):
        sys.stdout = self.old_stdout
        sys.stderr = self.old_stderr

    def test_simple_print(self):
        print_row(
            row=['a', 'b', 'c'],
            column_widths=[5, 3, 6],
            output_stream=self.stream,
            careful=True,
            quiet=False,
        )
        print_row(
            row=['aaa', 'bbbbbbbb', ''],
            column_widths=[5, 3, 6],
            output_stream=self.stream,
            careful=True,
            quiet=False,
        )
        first_row, second_row, _ = self.stream.getvalue().split('\n')
        self.assertEqual(first_row, '| a     | b   | c      |')
        self.assertEqual(second_row, '| aaa   | bbbbbbbb |        |')
        self.assertEqual(self.new_stdout.getvalue(), '')
        self.assertEqual(self.new_stderr.getvalue(), '')

    def test_careful(self):
        self.assertRaises(
            InputError,
            print_row,
            row=['a', 'b'],
            column_widths=[5, 3, 6],
            output_stream=self.stream,
            careful=True,
            quiet=False,
        )
        # Shouldn't print to stderr on exceptions
        self.assertRaises(
            InputError,
            print_row,
            row=['a', 'b', 'c'],
            column_widths=[5, 3],
            output_stream=self.stream,
            careful=True,
            quiet=True,
        )
        self.assertEqual(self.new_stdout.getvalue(), '')
        self.assertEqual(self.new_stderr.getvalue(), '')

    def test_quiet(self):
        print_row(
            row=['a', 'b'],
            column_widths=[5, 3, 6],
            output_stream=self.stream,
            careful=False,
            quiet=True,
        )
        print_row(
            row=['a', 'b', 'c'],
            column_widths=[5, 3],
            output_stream=self.stream,
            careful=False,
            quiet=True,
        )
        first_row, second_row, _ = self.stream.getvalue().split('\n')
        self.assertEqual(first_row, '| a     | b   |')
        self.assertEqual(second_row, '| a     | b   | c |')
        self.assertEqual(self.new_stdout.getvalue(), '')
        self.assertEqual(self.new_stderr.getvalue(), '')

    def test_not_quiet(self):
        print_row(
            row=['a', 'b'],
            column_widths=[5, 3, 6],
            output_stream=self.stream,
            careful=False,
            quiet=False,
        )
        self.assertEqual(self.new_stdout.getvalue(), '')
        self.assertTrue(self.new_stderr.getvalue().startswith('ERROR'))
        print_row(
            row=['a', 'b', 'c'],
            column_widths=[5, 3],
            output_stream=self.stream,
            careful=False,
            quiet=False,
        )
        self.assertEqual(self.new_stdout.getvalue(), '')
        self.assertTrue(self.new_stderr.getvalue().startswith('ERROR'))
