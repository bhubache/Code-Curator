from __future__ import annotations

import ast
import inspect
import textwrap
from typing import TYPE_CHECKING

from manim import Wait

if TYPE_CHECKING:
    from ast import FunctionDef
    from ast import Expr
    from typing import Any

def _get_run_time(func_ast, *, default: float) -> float:
    all_run_time_keywords = [attr for attr in func_ast.body[-1].body[-1].value.value.keywords if attr.arg == 'run_time']

    if len(all_run_time_keywords) == 0:
        return default

    if len(all_run_time_keywords) > 1:
        raise RuntimeError(f'More than one ``run_time`` arg found in {ast.unparse(func_ast)}!')
    # run_time_keyword = next(func_ast.body[-1].body[-1].value.value.keywords, None)

    keyword = all_run_time_keywords[0]

    try:
        return keyword.value.value
    except AttributeError:
        identifier = keyword.value.id

        breakpoint()



    return next((attr.value.value for attr in keywords if attr.arg == 'run_time'), default)


def _add_wait(run_time: float):
    pass


class _FuncNameInserter(ast.NodeTransformer):
    # def generic_visit(self, node: AST) -> AST:
    #     pass

    def visit_FunctionDef(self, node: FunctionDef) -> Any:
        # wait_yield = ast.Expr(
        #     ast.Yield(
        #         ast.Call(
        #             func=ast.Name(
        #                 'Wait',
        #                 ctx=node.body[-1].value.value.func.ctx,
        #             ),
        #             args=[
        #                 # ast.Constant(self.run_time),
        #                 ast.Constant(10),
        #             ],
        #             keywords=[],
        #         )
        #     )
        # )
        # node.body.append(wait_yield)
        node.body.insert(
            0,
            ast.Assign(
                targets=[
                    ast.Attribute(
                        value=ast.Name(
                            id='self',
                            ctx=ast.Load(),
                        ),
                        attr='func_name',
                        ctx=ast.Store(),
                    ),
                ],
                value=ast.Constant(
                    value=node.name,
                ),
            )
        )
        ast.fix_missing_locations(node)
        return node


class AutoAnimationTimer:
    @staticmethod
    def time(gen_method, owner, aligned_animation_script_owner) -> None:
        func_name = gen_method.__name__
        func_source = inspect.getsource(gen_method)
        func_source = textwrap.dedent(func_source)
        func_ast = ast.parse(func_source)
        # available_time = aligned_animation_script_owner.get_child(func_name).audio_duration
        # given_run_time = _get_run_time(func_ast, default=available_time)

        # if given_run_time > available_time:
        #     raise ValueError(f'{func_name} only has {available_time} second(s) of available time. Attempted: {given_run_time} second(s)')
        # 1. Check that the run_time if <= audio_duration
        # 2. Any extra time should be yielded as a wait animation after current animation

        # remaining_time = available_time - given_run_time
        # if remaining_time > 0:
        #     new_func_ast = _WaitAnimationAdder(remaining_time).visit(func_ast)
        #     new_code_obj = compile(new_func_ast, filename='', mode='exec')

        #     exec(new_code_obj, gen_method.__globals__, locals())
        #     return locals()[func_name]

        new_func_ast = _FuncNameInserter().visit(func_ast)
        new_code_obj = compile(new_func_ast, filename='', mode='exec')

        exec(new_code_obj, gen_method.__globals__, locals())
        return locals()[func_name]


        # return gen_method
