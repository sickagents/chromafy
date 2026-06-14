# 🎨 chromafy

A lightweight, zero-dependency Python library for adding colors, styles, gradients, and box drawing to terminal output. Works on Windows, macOS, and Linux with automatic terminal capability detection.

## Features

- 🎨 256-color and 24-bit true color support
- ✨ Bold, italic, underline, blink, and other text styles
- 🔲 Box drawing with Unicode characters (5 styles)
- 📊 Table formatting with auto-sizing columns
- 🌈 Gradient text generation
- 🎯 Automatic terminal capability detection (no garbage output in pipes)
- 🪶 Zero dependencies — pure Python, single file
- 🐍 Python 3.7+

## Installation

```bash
pip install chromafy
```

Or just copy `chromafy.py` into your project — it's a single file with no dependencies.

## Quick Start

```python
from chromafy import Color, Style, gradient, box, table

# Basic colors
print(Color.red("Error: something went wrong"))
print(Color.green("Success!"))
print(Color.yellow("Warning: check your config"))

# Combine colors and styles
print(Color.cyan(Style.bold("Important message")))
print(Color.magenta(Style.underline("Read this")))

# 256 colors
print(Color.color_256(196, "Hot red"))
print(Color.color_256(46, "Electric green"))

# True color (24-bit)
print(Color.rgb(255, 128, 0, "Orange"))
print(Color.rgb(100, 200, 255, "Sky blue"))

# Gradient text
print(gradient("Rainbow!", start=(255, 0, 0), end=(0, 0, 255)))

# Box drawing
print(box("Hello, World!", style="double", padding=2))
print(box("Alert!", style="heavy", border_color=Color.red))
print(box("Content", style="round", title=" My Box "))

# Table formatting
print(table(
    ["Name", "Role", "Score"],
    [
        ["Alice", "Engineer", "95"],
        ["Bob", "Designer", "88"],
        ["Charlie", "Manager", "92"],
    ],
    header_style=Style.bold
))

# Convenience aliases
from chromafy import red, green, bold, underline
print(red("Quick red text"))
print(green(bold("Bold green!")))
```

## API Reference

### `Color`

Static methods for coloring text:

| Method | Description |
|--------|-------------|
| `Color.red(text)` | Red text |
| `Color.green(text)` | Green text |
| `Color.yellow(text)` | Yellow text |
| `Color.blue(text)` | Blue text |
| `Color.magenta(text)` | Magenta text |
| `Color.cyan(text)` | Cyan text |
| `Color.white(text)` | White text |
| `Color.black(text)` | Black text |
| `Color.color_256(n, text)` | 256-color mode (0–255) |
| `Color.rgb(r, g, b, text)` | 24-bit true color foreground |
| `Color.bg_rgb(r, g, b, text)` | 24-bit true color background |

### `Style`

Static methods for text styling:

| Method | Description |
|--------|-------------|
| `Style.bold(text)` | **Bold** text |
| `Style.dim(text)` | Dimmed text |
| `Style.italic(text)` | *Italic* text |
| `Style.underline(text)` | Underlined text |
| `Style.blink(text)` | Blinking text |
| `Style.reverse(text)` | Reversed colors |
| `Style.strikethrough(text)` | ~~Strikethrough~~ text |
| `Style.overline(text)` | Overlined text |

### `gradient(text, start=(r,g,b), end=(r,g,b))`

Create a gradient between two RGB colors across the text.

```python
print(gradient("Hello World", start=(255, 0, 0), end=(0, 255, 0)))
```

### `box(text, style, padding, border_color, title)`

Draw a box around text. Available styles:

| Style | Characters |
|-------|-----------|
| `"single"` | `┌─┐│└─┘` |
| `"double"` | `╔═╗║╚═╝` |
| `"round"` | `╭─╮│╰─╯` |
| `"heavy"` | `┏━┓┃┗━┛` |
| `"ascii"` | `+-+\|+-+` |

```python
print(box("Hello!", style="double", padding=1, border_color=Color.cyan, title=" Greeting "))
```

### `table(headers, rows, border_color, header_style)`

Auto-sizing table with Unicode borders.

```python
print(table(
    ["Name", "Value"],
    [["Key1", "42"], ["Key2", "128"]],
    border_color=Color.blue,
    header_style=Style.bold
))
```

## Terminal Detection

Chromafy automatically detects whether stdout supports colors:

- **True color**: Terminal with `COLORTERM=truecolor` or `24bit`
- **256 color**: `TERM=xterm-256color` or similar
- **Basic 16 color**: Standard terminal
- **No color**: Piped output, `NO_COLOR` env var, or non-TTY

Override with `Color.force(True)` or `Color.force(False)`.

## `NO_COLOR` Support

Chromafy respects the [`NO_COLOR`](https://no-color.org/) convention. Set the `NO_COLOR` environment variable to disable all color output:

```bash
export NO_COLOR=1
```

## License

MIT
