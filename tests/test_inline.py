import markdown as md
import pytest

from markdown_math_escape import MathEscapeExtension

_test_patterns_inline = {
    "dollers_basic": (
        r"foo $2*\pi*r$ x$y$z",
        r"<p>foo \(2*\pi*r\) x\(y\)z</p>",
    ),
    "dollers_&lt;, &gt; and &amp;": (
        r"$x+y for x<0, y>0$ bar",
        r"<p>\(x+y for x&lt;0, y&gt;0\) bar</p>",
    ),
    "dollers_inside <p>": (
        r"<p>$2*\pi*r$</p>",
        r"<p>$2*\pi*r$</p>",
    ),
    "dollers_inside <s>": (
        r"<s>$2*\pi*r$</s>",
        r"<p><s>\(2*\pi*r\)</s></p>",
    ),
    "brackets_basic": (
        r"foo \(2*\pi*r\) x\(y\)z",
        r"<p>foo \(2*\pi*r\) x\(y\)z</p>",
    ),
    "brackets_&lt;, &gt; and &amp;": (
        r"\(x+y for x<0, y>0\) bar",
        r"<p>\(x+y for x&lt;0, y&gt;0\) bar</p>",
    ),
    "brackets_inside <p>": (
        r"<p>\(2*\pi*r\)</p>",
        r"<p>\(2*\pi*r\)</p>",
    ),
    "brackets_inside <s>": (
        r"<s>\(2*\pi*r\)</s>",
        r"<p><s>\(2*\pi*r\)</s></p>",
    ),
    "gitlab_basic": (
        r"foo $`2*\pi*r`$ x$`y`$z",
        r"<p>foo \(2*\pi*r\) x\(y\)z</p>",
    ),
    "gitlab_&lt; &gt; &amp;": (
        r"$`x+y for x<0, y>0`$ bar",
        r"<p>\(x+y for x&lt;0, y&gt;0\) bar</p>",
    ),
    "gitlab_inside <p>": (
        r"<p>$`2*\pi*r`$</p>",
        r"<p>$`2*\pi*r`$</p>",
    ),
    "gitlab_inside <s>": (
        r"<s>$`2*\pi*r`$</s>",
        r"<p><s>\(2*\pi*r\)</s></p>",
    ),
}


@pytest.mark.parametrize("key", list(_test_patterns_inline.keys()))
def test_inline(key):
    delimiters = key.split("_")[0]
    text, expected = _test_patterns_inline[key]
    actual = md.markdown(
        text,
        extensions=[
            MathEscapeExtension(delimiters=delimiters),
        ],
    )
    assert actual == expected
