from generic_ast.modules.optimizations.base import BaseTransformer
import ast_comments as ast


class getattr_transform(BaseTransformer):
    '''
        UnaryOp(
            op=USub(),
            operand=Constant(value=3))
    '''
    def visit_UnaryOp(self, node: ast.UnaryOp):
        if isinstance(node.op, ast.USub):
            if isinstance(node.operand, ast.Constant):
                if isinstance(node.operand.value, int):
                    return ast.Constant(value=-node.operand.value)
        elif isinstance(node.op, ast.Invert):
            if isinstance(node.operand, ast.Constant):
                if isinstance(node.operand.value, int):
                    return ast.Constant(value=~node.operand.value)
        return node