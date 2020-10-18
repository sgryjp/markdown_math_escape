# markdown_math_escape

![Test](https://github.com/sgryjp/markdown_math_escape/workflows/Test/badge.svg?branch=main)

[Python-Markdown](https://python-markdown.github.io/) extension to escape math expressions like `$2\pi$`.

## Description

This extension just **protects** math expressions in your markdown document
from being processed as markdown expression.
The math expressions you wrote will be kept as they were,
so that they can be rendered using [MathJax](https://www.mathjax.org/) or
[KaTeX](https://katex.org/) at client side (Web browsers).

## Installation

Firstly, install the extension by the command below:

    pip install git+https://github.com/sgryjp/markdown_math_escape.git

Then, let Python-Markdown to use it. For example:

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

Please refer to the ["Extensions" section](https://python-markdown.github.io/extensions/)
of official document for more detail.
