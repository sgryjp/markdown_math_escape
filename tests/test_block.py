import markdown as md
import pytest

from markdown_math_escape import MathEscapeExtension

_test_patterns_block = {
    "dollers_basic": (
        r"$$|2*\pi*r|$$(47)",
        r"$$|2*\pi*r|$$(47)",
    ),
    # "dollers_indent": (
    #     r"    $$|    2*\pi*r|    $$",
    #     r"    $$|    2*\pi*r|    $$",
    # ),
    "gitlab_backticks": (
        r"```math|2*\pi*r|```(32)",
        r"```math|2*\pi*r|```(32)",
    ),
    "gitlab_cascaded backticks": (
        r"````math|```math|2*\pi*r|```|````",
        r"````math|```math|2*\pi*r|```|````",
    ),
    "gitlab_tildes": (
        r"```math|~~~math|2*\pi*r|~~~|```",
        r"```math|~~~math|2*\pi*r|~~~|```",
    ),
    # "gitlab_indent": (
    #     r"    ```math|    2*\pi*r|    ```",
    #     r"    ```math|    2*\pi*r|    ```",
    # ),
}


@pytest.mark.parametrize("key", list(_test_patterns_block.keys()))
def test_block(key):
    delimiters = key.split("_")[0]
    text, expected = _test_patterns_block[key]
    actual = md.markdown(
        text.replace("|", "\n"),
        extensions=[
            "markdown.extensions.fenced_code",
            "markdown.extensions.codehilite",
            MathEscapeExtension(delimiters=delimiters),
        ],
    )
    assert actual.replace("\n", "|") == expected
