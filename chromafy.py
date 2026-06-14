"""
chromafy - A lightweight terminal color library for Python.

Zero dependencies. Works on Windows, macOS, and Linux.
Automatic terminal capability detection.
"""

import os
import re
import sys
from typing import Optional, Tuple

__version__ = "1.0.0"
__all__ = ["Color", "Style", "gradient", "box", "table"]

# Respect NO_COLOR convention (https://no-color.org/)
_NO_COLOR = os.environ.get("NO_COLOR") is not None


def _is_tty() -> bool:
    """Check if stdout is a TTY (interactive terminal)."""
    return hasattr(sys.stdout, "isatty") and sys.stdout.isatty()


def _supports_color() -> bool:
    """Detect if the terminal supports color output."""
    if _NO_COLOR:
        return False
    if not _is_tty():
        return False
    if sys.platform == "win32":
        # Windows 10+ supports ANSI via VT100
        try:
            import ctypes
            kernel32 = ctypes.windll.kernel32
            kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
            return True
        except Exception:
            return False
    return True


def _supports_256() -> bool:
    """Detect 256-color support."""
    term = os.environ.get("TERM", "")
    return "256color" in term or "24bit" in term


def _supports_truecolor() -> bool:
    """Detect 24-bit true color support."""
    colorterm = os.environ.get("COLORTERM", "")
    return colorterm in ("truecolor", "24bit")


class _ColorCapability:
    """Track terminal color capabilities."""
    NONE = 0
    BASIC = 1
    EXTENDED = 2    # 256 colors
    TRUECOLOR = 3   # 24-bit


def _get_capability() -> int:
    """Get the current terminal color capability level."""
    if not _supports_color():
        return _ColorCapability.NONE
    if _supports_truecolor():
        return _ColorCapability.TRUECOLOR
    if _supports_256():
        return _ColorCapability.EXTENDED
    return _ColorCapability.BASIC


# ANSI escape sequences
_ESC = "\033["
_RESET = f"{_ESC}0m"

# Regex for stripping ANSI escape codes
_ANSI_RE = re.compile(r"\x1b\[[0-9;]*m")


def _wrap(code: str, text: str) -> str:
    """Wrap text with ANSI escape codes if terminal supports it."""
    if _get_capability() == _ColorCapability.NONE:
        return text
    return f"{_ESC}{code}m{text}{_RESET}"


def _rgb_to_256(r: int, g: int, b: int) -> int:
    """Convert RGB to nearest 256-color code (6x6x6 cube, colors 16-231)."""
    ri = round(r / 255 * 5)
    gi = round(g / 255 * 5)
    bi = round(b / 255 * 5)
    return 16 + 36 * ri + 6 * gi + bi


def _wrap_rgb_fg(r: int, g: int, b: int, text: str) -> str:
    """Wrap text with 24-bit foreground color."""
    cap = _get_capability()
    if cap == _ColorCapability.NONE:
        return text
    if cap >= _ColorCapability.TRUECOLOR:
        return f"{_ESC}38;2;{r};{g};{b}m{text}{_RESET}"
    return _wrap(str(_rgb_to_256(r, g, b)), text)


def _wrap_rgb_bg(r: int, g: int, b: int, text: str) -> str:
    """Wrap text with 24-bit background color."""
    cap = _get_capability()
    if cap == _ColorCapability.NONE:
        return text
    if cap >= _ColorCapability.TRUECOLOR:
        return f"{_ESC}48;2;{r};{g};{b}m{text}{_RESET}"
    return f"{_ESC}48;5;{_rgb_to_256(r, g, b)}m{text}{_RESET}"


def _visible_len(s: str) -> int:
    """Calculate the visible length of a string, ignoring ANSI escape codes."""
    return len(_ANSI_RE.sub("", s))


class Color:
    """Terminal text coloring.

    All methods are static and return the colored string.
    Automatically degrades based on terminal capabilities.
    """

    _force: Optional[bool] = None

    @staticmethod
    def force(enable: Optional[bool] = None) -> None:
        """Force color on/off, or reset to auto-detect with None."""
        Color._force = enable

    @staticmethod
    def red(text: str) -> str:
        """Red text."""
        return _wrap("31", text)

    @staticmethod
    def green(text: str) -> str:
        """Green text."""
        return _wrap("32", text)

    @staticmethod
    def yellow(text: str) -> str:
        """Yellow text."""
        return _wrap("33", text)

    @staticmethod
    def blue(text: str) -> str:
        """Blue text."""
        return _wrap("34", text)

    @staticmethod
    def magenta(text: str) -> str:
        """Magenta text."""
        return _wrap("35", text)

    @staticmethod
    def cyan(text: str) -> str:
        """Cyan text."""
        return _wrap("36", text)

    @staticmethod
    def white(text: str) -> str:
        """White text."""
        return _wrap("37", text)

    @staticmethod
    def black(text: str) -> str:
        """Black text (useful on light backgrounds)."""
        return _wrap("30", text)

    @staticmethod
    def color_256(n: int, text: str) -> str:
        """256-color mode (0-255).

        Args:
            n: Color code (0-255).
            text: Text to colorize.

        Raises:
            ValueError: If n is outside 0-255.
        """
        if not 0 <= n <= 255:
            raise ValueError(f"Color code must be 0-255, got {n}")
        cap = _get_capability()
        if cap == _ColorCapability.NONE:
            return text
        if cap >= _ColorCapability.EXTENDED:
            return f"{_ESC}38;5;{n}m{text}{_RESET}"
        # Basic 16 color fallback
        return _wrap(str(n % 8 + 30), text)

    @staticmethod
    def rgb(r: int, g: int, b: int, text: str) -> str:
        """24-bit true color foreground (RGB 0-255 each).

        Falls back to nearest 256-color on terminals that don't support true color.
        """
        for val, name in [(r, "r"), (g, "g"), (b, "b")]:
            if not 0 <= val <= 255:
                raise ValueError(f"{name} must be 0-255, got {val}")
        return _wrap_rgb_fg(r, g, b, text)

    @staticmethod
    def bg_rgb(r: int, g: int, b: int, text: str) -> str:
        """24-bit true color background (RGB 0-255 each).

        Falls back to nearest 256-color on terminals that don't support true color.
        """
        for val, name in [(r, "r"), (g, "g"), (b, "b")]:
            if not 0 <= val <= 255:
                raise ValueError(f"{name} must be 0-255, got {val}")
        return _wrap_rgb_bg(r, g, b, text)


class Style:
    """Terminal text styling (bold, italic, underline, etc.)."""

    @staticmethod
    def bold(text: str) -> str:
        """Bold text."""
        return _wrap("1", text)

    @staticmethod
    def dim(text: str) -> str:
        """Dimmed / faint text."""
        return _wrap("2", text)

    @staticmethod
    def italic(text: str) -> str:
        """Italic text."""
        return _wrap("3", text)

    @staticmethod
    def underline(text: str) -> str:
        """Underlined text."""
        return _wrap("4", text)

    @staticmethod
    def blink(text: str) -> str:
        """Blinking text (not widely supported)."""
        return _wrap("5", text)

    @staticmethod
    def reverse(text: str) -> str:
        """Reversed foreground/background colors."""
        return _wrap("7", text)

    @staticmethod
    def strikethrough(text: str) -> str:
        """Strikethrough text."""
        return _wrap("9", text)

    @staticmethod
    def overline(text: str) -> str:
        """Overlined text."""
        return _wrap("53", text)


def gradient(
    text: str,
    start: Tuple[int, int, int] = (255, 0, 0),
    end: Tuple[int, int, int] = (0, 0, 255),
) -> str:
    """Create a gradient across text between two RGB colors.

    Args:
        text: The text to colorize.
        start: Starting RGB color tuple (r, g, b).
        end: Ending RGB color tuple (r, g, b).

    Returns:
        Text with gradient coloring applied.
    """
    if not text:
        return text

    cap = _get_capability()
    if cap == _ColorCapability.NONE:
        return text

    result = []
    length = len(text)

    for i, char in enumerate(text):
        ratio = 0.0 if length == 1 else i / (length - 1)

        r = int(start[0] + (end[0] - start[0]) * ratio)
        g = int(start[1] + (end[1] - start[1]) * ratio)
        b = int(start[2] + (end[2] - start[2]) * ratio)

        result.append(Color.rgb(r, g, b, char))

    return "".join(result)


# Box drawing character sets
_BOX_STYLES = {
    "single": {"tl": "┌", "tr": "┐", "bl": "└", "br": "┘", "h": "─", "v": "│"},
    "double": {"tl": "╔", "tr": "╗", "bl": "╚", "br": "╝", "h": "═", "v": "║"},
    "round":  {"tl": "╭", "tr": "╮", "bl": "╰", "br": "╯", "h": "─", "v": "│"},
    "heavy":  {"tl": "┏", "tr": "┓", "bl": "┗", "br": "┛", "h": "━", "v": "┃"},
    "ascii":  {"tl": "+", "tr": "+", "bl": "+", "br": "+", "h": "-", "v": "|"},
}


def box(
    text: str,
    style: str = "single",
    padding: int = 1,
    border_color: Optional[callable] = None,
    title: Optional[str] = None,
) -> str:
    """Draw a box around text using Unicode box-drawing characters.

    Args:
        text: Content to place inside the box.
        style: Box style — "single", "double", "round", "heavy", or "ascii".
        padding: Number of blank spaces around the content.
        border_color: Optional color function (e.g. Color.red) for border characters.
        title: Optional title text placed in the top border.

    Returns:
        The boxed string ready for printing.
    """
    if style not in _BOX_STYLES:
        raise ValueError(
            f"Unknown box style: {style!r}. Choose from: {list(_BOX_STYLES.keys())}"
        )

    chars = _BOX_STYLES[style]
    lines = text.split("\n")

    # Calculate content width from visible length (ignoring ANSI)
    max_width = max(_visible_len(line) for line in lines)
    content_width = max_width + padding * 2

    def _c(s: str) -> str:
        return border_color(s) if border_color else s

    result = []

    # Top border
    if title:
        title_vis = _visible_len(title)
        left_len = (content_width - title_vis - 2) // 2
        right_len = content_width - title_vis - 2 - left_len
        top = (
            _c(chars["tl"])
            + _c(chars["h"] * left_len)
            + title
            + _c(chars["h"] * right_len)
            + _c(chars["tr"])
        )
    else:
        top = _c(chars["tl"]) + _c(chars["h"] * content_width) + _c(chars["tr"])
    result.append(top)

    # Padding rows (top)
    pad_row = _c(chars["v"]) + " " * content_width + _c(chars["v"])
    for _ in range(padding):
        result.append(pad_row)

    # Content rows
    for line in lines:
        vis = _visible_len(line)
        right_pad = max_width - vis + padding
        row = (
            _c(chars["v"])
            + " " * padding
            + line
            + " " * right_pad
            + _c(chars["v"])
        )
        result.append(row)

    # Padding rows (bottom)
    for _ in range(padding):
        result.append(pad_row)

    # Bottom border
    bottom = _c(chars["bl"]) + _c(chars["h"] * content_width) + _c(chars["br"])
    result.append(bottom)

    return "\n".join(result)


def table(
    headers: list,
    rows: list,
    border_color: Optional[callable] = None,
    header_style: Optional[callable] = None,
) -> str:
    """Create a formatted table from headers and rows.

    Args:
        headers: List of column header strings.
        rows: List of rows, each a list of cell values.
        border_color: Optional color function for borders.
        header_style: Optional style function for headers.

    Returns:
        Formatted table string.
    """
    if not headers:
        return ""

    # Calculate column widths
    col_widths = [_visible_len(str(h)) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            if i < len(col_widths):
                col_widths[i] = max(col_widths[i], _visible_len(str(cell)))

    def _c(s: str) -> str:
        return border_color(s) if border_color else s

    def _h(s: str) -> str:
        return header_style(s) if header_style else s

    def _pad(text: str, width: int) -> str:
        vis = _visible_len(str(text))
        return str(text) + " " * (width - vis)

    result = []

    # Top border
    parts = [_c("─" * (w + 2)) for w in col_widths]
    result.append(_c("┌") + _c("┬").join(parts) + _c("┐"))

    # Header row
    cells = [_pad(h, col_widths[i]) for i, h in enumerate(headers)]
    result.append(
        _c("│ ") + _c(" │ ").join(_h(c) for c in cells) + _c(" │")
    )

    # Header separator
    parts = [_c("═" * (w + 2)) for w in col_widths]
    result.append(_c("╞") + _c("╪").join(parts) + _c("╡"))

    # Data rows
    for row in rows:
        cells = []
        for i in range(len(headers)):
            val = row[i] if i < len(row) else ""
            cells.append(_pad(val, col_widths[i]))
        result.append(
            _c("│ ") + _c(" │ ").join(cells) + _c(" │")
        )

    # Bottom border
    parts = [_c("─" * (w + 2)) for w in col_widths]
    result.append(_c("└") + _c("┴").join(parts) + _c("┘"))

    return "\n".join(result)


# Convenience aliases
red = Color.red
green = Color.green
yellow = Color.yellow
blue = Color.blue
magenta = Color.magenta
cyan = Color.cyan
white = Color.white
black = Color.black
bold = Style.bold
dim = Style.dim
italic = Style.italic
underline = Style.underline
