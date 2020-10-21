# markdown_math_escape

![Test](https://github.com/sgryjp/markdown_math_escape/workflows/Test/badge.svg?branch=main)

[Python-Markdown](https://python-markdown.github.io/) extension to escape math
expressions like `$e^{i\pi} + 1 = 0$`.

## Description

The benefits of using this extension are:

1. No special escaping syntax is needed
   - You can write `\left\{`, not `\left\\{`.
2. On writing, you are free to choose any delimiter style as you like
   - They will be converted to "brackets" styled delimiters so that they can be
     processed using [MathJax](https://www.mathjax.org/) or
     [KaTeX](https://katex.org/) without any configuration.
   - If you are using GitLab, you can choose `gitlab` delimiter style so that
     the file will be rendered with beautiful mathematics on GitLab.
3. It's fast
   - This extension _does not render_ mathematics

On the other hand:

- You need to setup either MathJax or KaTeX for client-side rendering
  - If you are using Nikola, you can use it's built-in feature to enable them
  - Otherwise, somehow you need to load and execute one of them
    (using a theme which supports them, for example)

Technically, this extension firstly protects math expressions from
Python-Markdown and its other extensions so that no unexpected (unhappy) change
will happen. Then it converts their delimiters (enclosing special characters)
to "brackets" styled delimiters... which is supported by default configuration
of MathJax and KaTeX.

## Installation

Firstly, install the extension by the command below:

    pip install markdown_math_escape

Secondly, you need to let Python-Markdown to use it. How to do it depends on
how you are using Python-Markdown. Please see [examples](#examples)
for an example which matches your usage.

## Options

The only available option is "`delimiters`" which specifies the type of
delimiters enclosing mathematics in your markdown files.
See the table below for supported values.

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

Note that this extension is compatible with [Nikola's built-in option to enable
MathJax or KaTeX](https://getnikola.com/handbook.html#math). Just set
`has_math` metadata field in your post to `true` and select MathJax or KaTeX by
specifying `USE_KATEX` value in `conf.py`.
