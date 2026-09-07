"""Minimal parser for the `export const X = <literal>;` data modules.

Reads the JS object/array literals in data/*.js without needing Node — handles
single/double/back-quoted strings, comments, trailing commas and bare keys.
"""

import re

_IDENT = re.compile(r'[A-Za-z_$][A-Za-z0-9_$]*')
_NUMBER = re.compile(r'-?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?')

_ESCAPES = {'n': '\n', 't': '\t', 'r': '\r', 'b': '\b', 'f': '\f',
            '0': '\0', '\\': '\\', "'": "'", '"': '"', '`': '`', '\n': ''}


class JSDataError(ValueError):
    pass


class _Parser:
    def __init__(self, src):
        self.s = src
        self.i = 0

    # ── helpers ──────────────────────────────────────────────────────────────

    def _skip(self):
        """Advance past whitespace and // or /* */ comments."""
        while self.i < len(self.s):
            c = self.s[self.i]
            if c in ' \t\r\n':
                self.i += 1
            elif self.s.startswith('//', self.i):
                nl = self.s.find('\n', self.i)
                self.i = len(self.s) if nl == -1 else nl + 1
            elif self.s.startswith('/*', self.i):
                end = self.s.find('*/', self.i + 2)
                if end == -1:
                    raise JSDataError('unterminated block comment')
                self.i = end + 2
            else:
                break

    def _expect(self, ch):
        self._skip()
        if self.i >= len(self.s) or self.s[self.i] != ch:
            got = self.s[self.i:self.i + 20] if self.i < len(self.s) else 'EOF'
            raise JSDataError(f'expected {ch!r} at {self.i}, got {got!r}')
        self.i += 1

    # ── values ───────────────────────────────────────────────────────────────

    def parse_value(self):
        self._skip()
        if self.i >= len(self.s):
            raise JSDataError('unexpected end of input')
        c = self.s[self.i]
        if c == '{':
            return self.parse_object()
        if c == '[':
            return self.parse_array()
        if c in '\'"`':
            return self.parse_string()
        m = _NUMBER.match(self.s, self.i)
        if m:
            self.i = m.end()
            text = m.group()
            return float(text) if ('.' in text or 'e' in text.lower()) else int(text)
        m = _IDENT.match(self.s, self.i)
        if m:
            self.i = m.end()
            word = m.group()
            if word == 'true':
                return True
            if word == 'false':
                return False
            if word in ('null', 'undefined'):
                return None
            raise JSDataError(f'unsupported identifier {word!r} at {m.start()}')
        raise JSDataError(f'unexpected character {c!r} at {self.i}')

    def parse_string(self):
        quote = self.s[self.i]
        self.i += 1
        out = []
        while self.i < len(self.s):
            c = self.s[self.i]
            if c == '\\':
                nxt = self.s[self.i + 1]
                if nxt == 'u':
                    out.append(chr(int(self.s[self.i + 2:self.i + 6], 16)))
                    self.i += 6
                    continue
                out.append(_ESCAPES.get(nxt, nxt))
                self.i += 2
                continue
            if c == quote:
                self.i += 1
                return ''.join(out)
            out.append(c)
            self.i += 1
        raise JSDataError('unterminated string')

    def parse_array(self):
        self._expect('[')
        items = []
        while True:
            self._skip()
            if self.i < len(self.s) and self.s[self.i] == ']':
                self.i += 1
                return items
            items.append(self.parse_value())
            self._skip()
            if self.i < len(self.s) and self.s[self.i] == ',':
                self.i += 1

    def parse_object(self):
        self._expect('{')
        obj = {}
        while True:
            self._skip()
            if self.i < len(self.s) and self.s[self.i] == '}':
                self.i += 1
                return obj
            if self.s[self.i] in '\'"`':
                key = self.parse_string()
            else:
                m = _IDENT.match(self.s, self.i)
                if not m:
                    raise JSDataError(f'bad object key at {self.i}')
                self.i = m.end()
                key = m.group()
            self._expect(':')
            obj[key] = self.parse_value()
            self._skip()
            if self.i < len(self.s) and self.s[self.i] == ',':
                self.i += 1


def load(path, name):
    """Return the value of `export const <name> = ...` from a JS module."""
    src = open(path, encoding='utf-8').read()
    m = re.search(r'export\s+const\s+' + re.escape(name) + r'\s*=', src)
    if not m:
        raise JSDataError(f'no `export const {name}` in {path}')
    p = _Parser(src)
    p.i = m.end()
    return p.parse_value()
