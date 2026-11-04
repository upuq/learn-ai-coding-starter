# Parser Conventions

These rules apply to `sloperator/parser/parser.py`.

## One method per grammar rule

- Give each grammar rule in `docs/spec.md` its own `Parser` method, named after the rule (`declaration`, `statement`, `expression`, `logic_or`, `primary`, ...).
- A method parses exactly its rule and returns that rule's AST node; it must not also handle a separate production inline.
- When several rules share a production, call the shared method instead of duplicating its parsing logic.
- Keep precedence levels as separate methods (`logic_or` → `logic_and` → `equality` → ... → `primary`) so the code mirrors the grammar.

## Syntax errors must say what token was found

- Report expectation failures through `self.expect(...)` or `self.error(...)`; both append `, found '<lexeme>'` or `, but reached end of file` at EOF.
- Write the message as the expectation only, e.g. `"expected ')' after parameters"`; `error()` supplies the found token.
- Raise `SlopSyntaxError` directly only for semantic checks that are not about an unexpected token, such as duplicate parameter names.
- Attach the offending token's line, never a hard-coded or unrelated line.
