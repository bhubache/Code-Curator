from __future__ import annotations

import ast
import inspect
import textwrap
from typing import TYPE_CHECKING

from code_curator.animations.utils import utils


if TYPE_CHECKING:
    from ast import FunctionDef
    from types import FunctionType


class _FuncNameInserter(ast.NodeTransformer):
    def __init__(self, name: str) -> None:
        self.name = name

    def visit_FunctionDef(self, node: FunctionDef) -> FunctionDef:  # noqa: N802
        node.body.insert(
            0,
            ast.Assign(
                targets=[
                    ast.Attribute(
                        value=ast.Name(
                            id="self",
                            ctx=ast.Load(),
                        ),
                        attr="func_name",
                        ctx=ast.Store(),
                    ),
                ],
                value=ast.Constant(
                    value=self.name,
                ),
            ),
        )
        ast.fix_missing_locations(node)
        return node


class AutoAnimationTimer:
    @staticmethod
    def time(gen_method, owner) -> FunctionType:
        if utils.is_overriding_start(gen_method.next):
            owner.animation_name_timing_map[
                gen_method.__name__
            ] -= utils.OVERRIDING_START_RUN_TIME_IN_SECONDS

        if utils.is_overriding_end(gen_method):
            owner.animation_name_timing_map[
                gen_method.__name__
            ] -= utils.OVERRIDING_END_RUN_TIME_IN_SECONDS

        func_name = gen_method.__name__
        func_source = inspect.getsource(gen_method)
        func_source = textwrap.dedent(func_source)
        func_ast = ast.parse(func_source)

        new_func_ast = _FuncNameInserter(name=func_name).visit(func_ast)
        new_code_obj = compile(new_func_ast, filename="", mode="exec")

        exec(new_code_obj, gen_method.__globals__, locals())  # noqa: SCS101
        try:
            return locals()[func_name]
        except KeyError:
            return locals()["_wait"]
