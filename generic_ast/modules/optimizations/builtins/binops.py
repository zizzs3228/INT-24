from generic_ast.modules.optimizations.base import BaseTransformer
import ast_comments as ast
import builtins


class getattr_transform(BaseTransformer):
    def visit_BinOp(self, node: ast.BinOp):
        ### ints
        if isinstance(node.op, ast.Pow):
            if isinstance(node.left, ast.Constant) and isinstance(node.right, ast.Constant):
                if isinstance(node.left.value, int) and isinstance(node.right.value, int):
                    return ast.Constant(value=node.left.value ** node.right.value)
        elif isinstance(node.op, ast.Mult):
            if isinstance(node.left, ast.Constant) and isinstance(node.right, ast.Constant):
                if isinstance(node.left.value, int) and isinstance(node.right.value, int):
                    return ast.Constant(value=node.left.value * node.right.value)
        elif isinstance(node.op, ast.Div):
            if isinstance(node.left, ast.Constant) and isinstance(node.right, ast.Constant):
                if isinstance(node.left.value, int) and isinstance(node.right.value, int):
                    return ast.Constant(value=node.left.value / node.right.value)
        elif isinstance(node.op, ast.FloorDiv):
            if isinstance(node.left, ast.Constant) and isinstance(node.right, ast.Constant):
                if isinstance(node.left.value, int) and isinstance(node.right.value, int):
                    return ast.Constant(value=node.left.value // node.right.value)
        elif isinstance(node.op, ast.Mod):
            if isinstance(node.left, ast.Constant) and isinstance(node.right, ast.Constant):
                if isinstance(node.left.value, int) and isinstance(node.right.value, int):
                    return ast.Constant(value=node.left.value % node.right.value)
        elif isinstance(node.op, ast.Add):
            if isinstance(node.left, ast.Constant) and isinstance(node.right, ast.Constant):
                if isinstance(node.left.value, int) and isinstance(node.right.value, int):
                    return ast.Constant(value=node.left.value + node.right.value)
        elif isinstance(node.op, ast.Sub):
            if isinstance(node.left, ast.Constant) and isinstance(node.right, ast.Constant):
                if isinstance(node.left.value, int) and isinstance(node.right.value, int):
                    return ast.Constant(value=node.left.value - node.right.value)
        elif isinstance(node.op, ast.BitAnd):
            if isinstance(node.left, ast.Constant) and isinstance(node.right, ast.Constant):
                if isinstance(node.left.value, int) and isinstance(node.right.value, int):
                    return ast.Constant(value=node.left.value & node.right.value)
        elif isinstance(node.op, ast.BitXor):
            if isinstance(node.left, ast.Constant) and isinstance(node.right, ast.Constant):
                if isinstance(node.left.value, int) and isinstance(node.right.value, int):
                    return ast.Constant(value=node.left.value ^ node.right.value)
        elif isinstance(node.op, ast.BitOr):
            if isinstance(node.left, ast.Constant) and isinstance(node.right, ast.Constant):
                if isinstance(node.left.value, int) and isinstance(node.right.value, int):
                    return ast.Constant(value=node.left.value | node.right.value)
        elif isinstance(node.op, ast.LShift):
            if isinstance(node.left, ast.Constant) and isinstance(node.right, ast.Constant):
                if isinstance(node.left.value, int) and isinstance(node.right.value, int):
                    return ast.Constant(value=node.left.value << node.right.value)
        elif isinstance(node.op, ast.RShift):
            if isinstance(node.left, ast.Constant) and isinstance(node.right, ast.Constant):
                if isinstance(node.left.value, int) and isinstance(node.right.value, int):
                    return ast.Constant(value=node.left.value >> node.right.value)
        ### ints
                
                
        ###strs
        if isinstance(node.op, ast.Add):
            if isinstance(node.left, ast.Constant) and isinstance(node.right, ast.Constant):
                if isinstance(node.left.value, str) and isinstance(node.right.value, str):
                    return ast.Constant(value=node.left.value + node.right.value)
        return node
