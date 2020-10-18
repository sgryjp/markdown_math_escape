# markdown_math_escape

![Test](https://github.com/sgryjp/markdown_math_escape/workflows/Test/badge.svg?branch=main)

[Python-Markdown](https://python-markdown.github.io/) extension to escape math
expressions like `$e^{i\pi} + 1 = 0$`.

## Description

This extension protects math expressions from markdown parser so that no
unexpected change will happen. Then, it converts their delimiters (enclosing
special characters) to "brackets" styled delimiters which is supported by both
[MathJax](https://www.mathjax.org/) and [KaTeX](https://katex.org/).
Since this extension does not render mathematics by itself:

- Pros: It does not slow markdown processing down... it's very fast.
- Cons: You need to setup either MathJax or KaTeX for client-side rendering.

From a user point of view, you can choose delimiters for writing as you like
and you do not need to worry about conflict between markdown syntax and TeX
syntax.

## Installation

Firstly, install the extension by the command below:

    pip install git+https://github.com/sgryjp/markdown_math_escape.git

Secondly, you need to let Python-Markdown to use it. How to do it depends on
how you are using Python-Markdown. Please see [examples section](#examples)
and find an example which is similar to your usage.

## Options

An option `delimiters` is available. See the table below for supported values.

<table>
    <thead>
        <tr>
            <th><code>delimiters</code></th>
            <th>Inline (non-display mode)</th>
            <th>Display mode math</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><code>dollers</code></td>
            <td><code>$e^{i\pi} + 1 = 0$</code></td>
            <td><pre>$$
e^{i\pi} + 1 = 0
$$</pre></td>
        </tr>
        <tr>
            <td><code>brackets</code></td>
            <td><code>\(e^{i\pi} + 1 = 0\)</code></td>
            <td><pre>\[
e^{i\pi} + 1 = 0
\]</pre></td>
        </tr>
        <tr>
            <td><code>gitlab</code></td>
            <td><code>$`e^{i\pi} + 1 = 0`$</code></td>
            <td><pre>```math
e^{i\pi} + 1 = 0
```</pre></td>
        </tr>
    </tbody>
</table>


## Examples

### Python script

If you are using Python-Markdown directly in your Python script (or library),
just do so in the standard way. For example:

```python
import markdown as md
from markdown_math_escape import MathEscapeExtension

md.markdown(
    some_text,
    extensions=[
        "markdown.extensions.codehilite",
        "markdown.extensions.extra",
        MathEscapeExtension(delimiters="dollers"),
    ],
)
```

Please refer to the
[Python-Markdown's document](https://python-markdown.github.io/extensions/)
for more details.

### Pelican

If you are using Python-Markdown as part of
[Pelican](https://blog.getpelican.com/),
you can use extension name `markdown_math_escape`. For example:

```python
# pelicanconf.py
MARKDOWN = {
    'extension_configs': {
        # ...other extensions...
        "markdown_math_escape": {"delimiters": "dollers"},
    }
}
```

Please refer to the
[Pelican's document](https://docs.getpelican.com/en/stable/settings.html)
for more details.

### Nikola

If you are using Python-Markdown as part of
[Nikola](https://getnikola.com/),
you can use extension name `markdown_math_escape`. For example:

```python
# conf.py
MARKDOWN_EXTENSIONS = [
    # ...other extensions...
    'markdown_math_escape',
]

MARKDOWN_EXTENSION_CONFIGS = {
    DEFAULT_LANG: {
        "markdown_math_escape": {"delimiters": "dollers"},
    },
}
```
