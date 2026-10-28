"""
PA 2: The USILang Lexer -- starter.

Complete tokenize() below. See the assignment, Part B,
for the full requirements. Must use a single compiled master regex
with named groups -- not a hand-rolled character-by-character loop.
"""

import re
from dataclasses import dataclass
from typing import List


import re
from dataclasses import dataclass


@dataclass
class Token:
    type: str
    lexeme: str
    line: int


class LexError(Exception):
    pass


KEYWORDS = {"let": "LET"}

TOKEN_SPEC = [
    ("NUMBER",     r"\d+"),
    ("IDENT",      r"[A-Za-z_][A-Za-z0-9_]*"),
    ("PLUS",       r"\+"),
    ("MINUS",      r"-"),
    ("STAR",       r"\*"),
    ("SLASH",      r"/"),
    ("LPAREN",     r"\("),
    ("RPAREN",     r"\)"),
    ("ASSIGN",     r"="),
    ("SEMI",       r";"),
    ("NEWLINE",    r"\n"),
    ("WHITESPACE", r"[ \t]+"),
    ("COMMENT",    r"#[^\n]*"),
]

_MASTER = re.compile(
    "|".join(f"(?P<{name}>{pattern})" for name, pattern in TOKEN_SPEC)
)

_SKIP = {"WHITESPACE", "COMMENT"}


def tokenize(source: str) -> list[Token]:
    tokens: list[Token] = []
    pos = 0
    line = 1
    length = len(source)

    while pos < length:
        match = _MASTER.match(source, pos)
        if match is None:
            raise LexError(
                f"Unexpected character {source[pos]!r} at line {line}"
            )

        kind = match.lastgroup
        lexeme = match.group()

        if kind == "NEWLINE":
            line += 1
        elif kind in _SKIP:
            pass
        else:
            if kind == "IDENT" and lexeme in KEYWORDS:
                kind = KEYWORDS[lexeme]
            tokens.append(Token(kind, lexeme, line))

        pos = match.end()

    tokens.append(Token("EOF", "", line))
    return tokens
