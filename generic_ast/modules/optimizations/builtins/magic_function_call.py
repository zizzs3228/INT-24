from generic_ast.modules.optimizations.base import BaseTransformer
import ast_comments as ast
import io


import builtins


class StrMagicMethod(BaseTransformer):

    def leave_Call(self, node: ast.Call):
        if isinstance(node.func, ast.Attribute):
            if isinstance(node.func.value, ast.Name):
                if node.func.attr == "__str__":
                    return node
        return node

