"""Tests for chromafy terminal color library."""

import os
import sys
import unittest

# Force color off for testing (we test string generation, not terminal rendering)
os.environ["NO_COLOR"] = "1"

sys.path.insert(0, os.path.dirname(__file__))
import chromafy
from chromafy import Color, Style, gradient, box, table, _visible_len


class TestColor(unittest.TestCase):
    """Test Color class methods."""

    def test_red_returns_plain_text(self):
        self.assertEqual(Color.red("hello"), "hello")

    def test_green_returns_plain_text(self):
        self.assertEqual(Color.green("hello"), "hello")

    def test_yellow_returns_plain_text(self):
        self.assertEqual(Color.yellow("hello"), "hello")

    def test_blue_returns_plain_text(self):
        self.assertEqual(Color.blue("hello"), "hello")

    def test_magenta_returns_plain_text(self):
        self.assertEqual(Color.magenta("hello"), "hello")

    def test_cyan_returns_plain_text(self):
        self.assertEqual(Color.cyan("hello"), "hello")

    def test_white_returns_plain_text(self):
        self.assertEqual(Color.white("hello"), "hello")

    def test_black_returns_plain_text(self):
        self.assertEqual(Color.black("hello"), "hello")

    def test_color_256_valid_range(self):
        self.assertEqual(Color.color_256(0, "test"), "test")
        self.assertEqual(Color.color_256(128, "test"), "test")
        self.assertEqual(Color.color_256(255, "test"), "test")

    def test_color_256_invalid_range(self):
        with self.assertRaises(ValueError):
            Color.color_256(-1, "test")
        with self.assertRaises(ValueError):
            Color.color_256(256, "test")

    def test_rgb_valid(self):
        self.assertEqual(Color.rgb(255, 0, 0, "red"), "red")
        self.assertEqual(Color.rgb(0, 255, 0, "green"), "green")
        self.assertEqual(Color.rgb(0, 0, 255, "blue"), "blue")

    def test_rgb_invalid(self):
        with self.assertRaises(ValueError):
            Color.rgb(256, 0, 0, "test")
        with self.assertRaises(ValueError):
            Color.rgb(-1, 0, 0, "test")
        with self.assertRaises(ValueError):
            Color.rgb(0, 300, 0, "test")

    def test_bg_rgb_valid(self):
        self.assertEqual(Color.bg_rgb(100, 200, 50, "test"), "test")

    def test_bg_rgb_invalid(self):
        with self.assertRaises(ValueError):
            Color.bg_rgb(0, 0, -1, "test")
        with self.assertRaises(ValueError):
            Color.bg_rgb(0, 0, 256, "test")


class TestStyle(unittest.TestCase):
    """Test Style class methods."""

    def test_bold(self):
        self.assertEqual(Style.bold("test"), "test")

    def test_dim(self):
        self.assertEqual(Style.dim("test"), "test")

    def test_italic(self):
        self.assertEqual(Style.italic("test"), "test")

    def test_underline(self):
        self.assertEqual(Style.underline("test"), "test")

    def test_blink(self):
        self.assertEqual(Style.blink("test"), "test")

    def test_reverse(self):
        self.assertEqual(Style.reverse("test"), "test")

    def test_strikethrough(self):
        self.assertEqual(Style.strikethrough("test"), "test")

    def test_overline(self):
        self.assertEqual(Style.overline("test"), "test")


class TestGradient(unittest.TestCase):
    """Test gradient function."""

    def test_gradient_plain_text(self):
        result = gradient("hello", start=(255, 0, 0), end=(0, 0, 255))
        self.assertEqual(result, "hello")

    def test_gradient_empty_string(self):
        result = gradient("", start=(255, 0, 0), end=(0, 0, 255))
        self.assertEqual(result, "")

    def test_gradient_single_char(self):
        result = gradient("X", start=(255, 0, 0), end=(0, 0, 255))
        self.assertEqual(result, "X")

    def test_gradient_default_colors(self):
        result = gradient("test")
        self.assertEqual(result, "test")


class TestBox(unittest.TestCase):
    """Test box function."""

    def test_box_single_style(self):
        result = box("Hello", style="single")
        self.assertIn("Hello", result)
        self.assertIn("┌", result)
        self.assertIn("┐", result)
        self.assertIn("└", result)
        self.assertIn("┘", result)
        self.assertIn("─", result)
        self.assertIn("│", result)

    def test_box_double_style(self):
        result = box("Test", style="double")
        self.assertIn("Test", result)
        self.assertIn("╔", result)
        self.assertIn("╝", result)
        self.assertIn("═", result)
        self.assertIn("║", result)

    def test_box_round_style(self):
        result = box("Round", style="round")
        self.assertIn("╭", result)
        self.assertIn("╯", result)

    def test_box_heavy_style(self):
        result = box("Heavy", style="heavy")
        self.assertIn("┏", result)
        self.assertIn("┛", result)
        self.assertIn("━", result)
        self.assertIn("┃", result)

    def test_box_ascii_style(self):
        result = box("ASCII", style="ascii")
        self.assertIn("+", result)
        self.assertIn("-", result)
        self.assertIn("|", result)

    def test_box_invalid_style(self):
        with self.assertRaises(ValueError):
            box("test", style="nonexistent")

    def test_box_with_title(self):
        result = box("Content", title="Title")
        self.assertIn("Title", result)
        self.assertIn("Content", result)

    def test_box_with_padding(self):
        result = box("Pad", padding=3)
        self.assertIn("Pad", result)
        lines = result.split("\n")
        # Should have: top + 3 pad + 1 content + 3 pad + bottom = 9 lines
        self.assertEqual(len(lines), 9)

    def test_box_multiline(self):
        result = box("Line 1\nLine 2\nLine 3")
        self.assertIn("Line 1", result)
        self.assertIn("Line 2", result)
        self.assertIn("Line 3", result)

    def test_box_with_border_color(self):
        result = box("test", border_color=Color.red)
        self.assertIn("test", result)

    def test_box_default_style(self):
        """Default style should be 'single'."""
        result = box("test")
        self.assertIn("┌", result)
        self.assertIn("┘", result)

    def test_box_padding_default(self):
        """Default padding should be 1."""
        result = box("X")
        lines = result.split("\n")
        # top + 1 pad + 1 content + 1 pad + bottom = 5 lines
        self.assertEqual(len(lines), 5)


class TestTable(unittest.TestCase):
    """Test table function."""

    def test_basic_table(self):
        result = table(["Name", "Age"], [["Alice", "30"], ["Bob", "25"]])
        self.assertIn("Name", result)
        self.assertIn("Age", result)
        self.assertIn("Alice", result)
        self.assertIn("30", result)
        self.assertIn("Bob", result)
        self.assertIn("25", result)
        # Should have borders
        self.assertIn("┌", result)
        self.assertIn("┘", result)
        self.assertIn("╞", result)
        self.assertIn("╡", result)

    def test_empty_headers(self):
        result = table([], [])
        self.assertEqual(result, "")

    def test_table_with_border_color(self):
        result = table(["A"], [["1"]], border_color=Color.cyan)
        self.assertIn("A", result)
        self.assertIn("1", result)

    def test_table_with_header_style(self):
        result = table(["Col"], [["val"]], header_style=Style.bold)
        self.assertIn("Col", result)
        self.assertIn("val", result)

    def test_table_auto_sizing(self):
        """Columns should auto-size to fit the widest cell."""
        result = table(["A", "Long Header"], [["short", "x"]])
        lines = result.split("\n")
        # All lines should have equal width borders
        border_line = lines[0]  # top border
        self.assertIn("─", border_line)

    def test_table_empty_rows(self):
        result = table(["Col1", "Col2"], [])
        self.assertIn("Col1", result)
        self.assertIn("Col2", result)

    def test_table_missing_cells(self):
        """Rows with fewer cells than headers should be padded."""
        result = table(["A", "B", "C"], [["only_one"]])
        self.assertIn("only_one", result)
        self.assertIn("A", result)
        self.assertIn("C", result)


class TestVisibleLen(unittest.TestCase):
    """Test the _visible_len helper."""

    def test_plain_text(self):
        self.assertEqual(_visible_len("hello"), 5)

    def test_empty_string(self):
        self.assertEqual(_visible_len(""), 0)

    def test_with_ansi_codes(self):
        # Manually construct ANSI-wrapped text
        ansi_text = "\033[31mhello\033[0m"
        self.assertEqual(_visible_len(ansi_text), 5)

    def test_multiple_ansi_codes(self):
        ansi_text = "\033[1;31mhello\033[0m world"
        self.assertEqual(_visible_len(ansi_text), 11)


class TestConvenienceAliases(unittest.TestCase):
    """Test module-level convenience aliases."""

    def test_aliases_exist(self):
        self.assertTrue(callable(chromafy.red))
        self.assertTrue(callable(chromafy.green))
        self.assertTrue(callable(chromafy.yellow))
        self.assertTrue(callable(chromafy.blue))
        self.assertTrue(callable(chromafy.magenta))
        self.assertTrue(callable(chromafy.cyan))
        self.assertTrue(callable(chromafy.white))
        self.assertTrue(callable(chromafy.black))
        self.assertTrue(callable(chromafy.bold))
        self.assertTrue(callable(chromafy.dim))
        self.assertTrue(callable(chromafy.italic))
        self.assertTrue(callable(chromafy.underline))

    def test_aliases_work(self):
        self.assertEqual(chromafy.red("x"), "x")
        self.assertEqual(chromafy.bold("x"), "x")
        self.assertEqual(chromafy.underline("x"), "x")

    def test_aliases_match_class_methods(self):
        self.assertEqual(chromafy.red("t"), Color.red("t"))
        self.assertEqual(chromafy.green("t"), Color.green("t"))
        self.assertEqual(chromafy.bold("t"), Style.bold("t"))


class TestVersion(unittest.TestCase):
    """Test version attribute."""

    def test_version_exists(self):
        self.assertTrue(hasattr(chromafy, "__version__"))

    def test_version_format(self):
        parts = chromafy.__version__.split(".")
        self.assertEqual(len(parts), 3)
        for part in parts:
            self.assertTrue(part.isdigit())


if __name__ == "__main__":
    unittest.main()
