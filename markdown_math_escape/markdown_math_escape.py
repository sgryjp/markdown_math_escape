import io
import re
import xml.etree.ElementTree as etree
from base64 import b64decode, b64encode
from typing import List, Match

import markdown
import markdown.blockprocessors
import markdown.extensions
import markdown.inlinepatterns
import markdown.postprocessors
import markdown.preprocessors

_default_delimiters = "dollers"

_re_dollers_inline = re.compile(r"(?<!\\)\$(?!\$)(?P<expr>[^\$]*)(?<!\\)\$(?!\$)")
_re_dollers_block_begin = re.compile(r"^(?P<indent>\s*)(?P<fence>\$\$)")
_re_dollers_block_end = _re_dollers_block_begin

_re_gitlab_inline = re.compile(r"(?<!\\)\$`(?P<expr>[^`]*)`\$")
_re_gitlab_block_begin = re.compile(r"^(?P<indent>\s*)(?P<fence>```+|~~~+)math")
_re_gitlab_block_end = re.compile(
    r"^(?P<indent>\s*)(?P<fence>```+|~~~+)(?:\s*\((?P<eqno>\d+)\))?$"
)

_re_escaped_inline_math = re.compile(
    r'<code class="--markdown-math-escape">([A-Za-z0-9+/=]+)</code>'
)
_escaped_block_math_begin = '<pre class="--markdown-math-escape">'


_profiles = {
    "dollers": {
        "make_inline": lambda expr: f"${expr}$",
        "re_inline": _re_dollers_inline,
        "re_block_begin": _re_dollers_block_begin,
        "re_block_end": _re_dollers_block_end,
    },
    "gitlab": {
        "make_inline": lambda expr: f"$`{expr}`$",
        "re_inline": _re_gitlab_inline,
        "re_block_begin": _re_gitlab_block_begin,
        "re_block_end": _re_gitlab_block_end,
    },
}


def _encode(s: str) -> str:
    s = s.replace("&", "&amp;")
    s = s.replace("<", "&lt;")
    s = s.replace(">", "&gt;")
    return b64encode(s.encode("utf-8")).decode("utf-8")


def _decode(s: str) -> str:
    return b64decode(s.encode("utf-8")).decode("utf-8")


def makeExtension(**kwargs):
    """Register this extension to Python-Markdown."""
    return MathEscapeExtension(**kwargs)


class MathEscapeExtension(markdown.extensions.Extension):
    def __init__(self, **kwargs):
        self.config = {
            "delimiters": [
                _default_delimiters,
                "Delimiters surrounding math expressions.",
            ],
        }
        super(MathEscapeExtension, self).__init__(**kwargs)

    def extendMarkdown(self, md):
        delimiters = self.getConfig("delimiters")

        md.preprocessors.register(
            MathEscapePreprocessor(md, delimiters),
            "math_escape",
            priority=1000,
        )
        md.postprocessors.register(
            MathEscapePostprocessor(md, delimiters),
            "math_escape",
            priority=0,
        )
        md.inlinePatterns.register(
            MathEscapeInlineProcessor(md, delimiters),
            "math_escape",
            priority=1000,
        )


class MathEscapePreprocessor(markdown.preprocessors.Preprocessor):
    def __init__(self, md, delimiters):
        self._re_block_begin = _profiles[delimiters]["re_block_begin"]
        self._re_block_end = _profiles[delimiters]["re_block_end"]
        super().__init__(md)

    def run(self, lines: List[str]):
        i = 0
        while i < len(lines):
            match1 = self._re_block_begin.match(lines[i])
            if match1:
                j = self._find_closing_pair(lines, i, match1)
                if 0 <= j:
                    tag = '<pre class="--markdown-math-escape">'
                    lines[i] = tag + lines[i]
                    for k in range(i + 1, j):
                        lines[k] = _encode(lines[k])
                    lines[j] = lines[j] + "</pre>"
                    i = j
            i += 1
        return lines

    def _find_closing_pair(self, lines: List[str], i, match):
        for j in range(i + 1, len(lines)):
            match2 = self._re_block_end.match(lines[j])
            if (
                match2
                and match2.group("indent") == match.group("indent")
                and match2.group("fence") == match.group("fence")
            ):
                return j
        return -1


class MathEscapePostprocessor(markdown.postprocessors.Postprocessor):
    def __init__(self, md, delimiters):
        self._make_inline = _profiles[delimiters]["make_inline"]
        super().__init__(md)

    def run(self, text: str):
        lines = []
        newline = "\n"
        istream = io.StringIO(text)
        try:
            in_block = False
            for i, line in enumerate(istream):
                # Use the new line code used for the first line
                if i == 0:
                    match = re.search(r"\r?\n$", line, re.MULTILINE)
                    if match:
                        newline = match.group(0)

                # Replace blocks
                if not in_block and _escaped_block_math_begin in line:
                    in_block = True
                    lines.append(
                        line.rstrip("\r\n").replace(_escaped_block_math_begin, "")
                    )
                elif in_block and "</pre>" in line:
                    in_block = False
                    lines.append(line.rstrip("\r\n").replace("</pre>", "", 1))
                elif in_block:
                    decoded = _decode(line.rstrip())
                    lines.append(decoded)
                else:  # if not inside a math block
                    tokens = []
                    offset = 0
                    while True:
                        match = _re_escaped_inline_math.search(line, offset)
                        if not match:
                            break
                        mathexpr = _decode(match.group(1))
                        tokens.append(
                            line[offset : match.start()] + self._make_inline(mathexpr)
                        )
                        offset = match.end()
                    tokens.append(line[offset:])
                    lines.append("".join(tokens))
            return newline.join(lines)
        finally:
            istream.close()


class MathEscapeInlineProcessor(markdown.inlinepatterns.InlineProcessor):
    def __init__(self, md, delimiters):
        pattern = _profiles[delimiters]["re_inline"].pattern
        super().__init__(pattern, md)

    def handleMatch(self, match: Match, data: str):
        elm = etree.Element("code")
        elm.set("class", "--markdown-math-escape")
        elm.text = _encode(match.group(1))
        return elm, match.start(0), match.end(0)
