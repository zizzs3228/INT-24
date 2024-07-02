from generic_ast.modules.optimizations.base import BaseTransformer
import ast_comments as ast


class Indexes(BaseTransformer):
    def visit_Subscript(self, node: ast.Subscript):
        '''
            Subscript(
                value=Constant(value='<built-in function oct>'),
                slice=Constant(value=-3),
                ctx=Load()),
        '''
        if isinstance(node.slice, ast.Constant) and isinstance(node.value, ast.Constant):
            if isinstance(node.slice.value, int) and isinstance(node.value.value, str):
                return ast.Constant(value=node.value.value[node.slice.value])
        return node
