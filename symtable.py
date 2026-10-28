"""
PA 4: The USILang Symbol Table -- starter.

Complete Environment and check_program below. See
PA_04_The_USILang_Symbol_Table.md, Part B, for the full requirements.
"""

from typing import Optional

from parser import Assignment, BinOp, Declaration, Number, Program, Variable


class SemanticError(Exception):
    pass


class Environment:
    def __init__(self, parent: Optional["Environment"] = None) -> None:
        self.parent = parent
        self._names: dict = {}

    def define(self, name: str, line: int) -> None:
        """
        Store name -> line in THIS scope. Raise SemanticError if `name`
        is already defined in THIS scope (not a parent scope --
        shadowing a parent name is allowed).
        """
        if name in self._names:
            original_line = self._names[name]
            raise SemanticError(
                f"Duplicate declaration of '{name}' (line {line}; originally declared line {original_line})."
            )
        self._names[name] = line

    def resolve(self, name: str) -> int:
        """
        Look up `name` in this scope, then climb `parent` links.
        Return the declaration line, or raise SemanticError if not
        found anywhere in the chain.
        """
        env = self
        while env is not None:
            if name in env._names:
                return env._names[name]
            env = env.parent
        raise SemanticError(f"Undeclared variable '{name}'.")


def _check_expr(expr, env: Environment) -> None:
    """Recursively resolve every Variable reference inside an expression."""
    if isinstance(expr, Number):
        return
    if isinstance(expr, Variable):
        try:
            env.resolve(expr.name)
        except SemanticError:
            raise SemanticError(
                f"Use of undeclared variable '{expr.name}' (line {expr.line})."
            ) from None
        return
    if isinstance(expr, BinOp):
        _check_expr(expr.left, env)
        _check_expr(expr.right, env)
        return
    raise SemanticError(f"Unknown expression node: {expr!r}")


def check_program(ast: Program) -> Environment:
    env = Environment()
    for stmt in ast.statements:
        if isinstance(stmt, Declaration):
            _check_expr(stmt.expr, env)
            env.define(stmt.name, stmt.line)
        elif isinstance(stmt, Assignment):
            try:
                env.resolve(stmt.name)
            except SemanticError:
                raise SemanticError(
                    f"Use of undeclared variable '{stmt.name}' (line {stmt.line})."
                ) from None
            _check_expr(stmt.expr, env)
        else:
            raise SemanticError(f"Unknown statement node: {stmt!r}")
    return env
