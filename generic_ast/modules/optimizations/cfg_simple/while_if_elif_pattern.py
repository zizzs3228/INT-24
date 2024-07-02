from generic_ast.modules.optimizations.base import BaseTransformer
import ast_comments as ast
import operator


class WhileIfElifPattern(BaseTransformer):
    def generic_leave(self, node: ast.Module):
        if not hasattr(node, "body"):
            return node
        if not len(node.body) >= 2:
            return node
        if not isinstance(node.body[0], ast.Assign) or \
                not isinstance(node.body[1], ast.While):
            return node

        assign_node: ast.Assign = node.body[0]
        while_node: ast.While = node.body[1]

        if len(assign_node.targets) > 1:
            return node
        if not isinstance(assign_node.targets[0], ast.Name):
            return node

        if not isinstance(assign_node.value, ast.Constant):
            return node

        current_value: int = assign_node.value.value
        dispatch_varname: str = assign_node.targets[0].id

        if len(while_node.body) > 1:
            return node
        if not isinstance(while_node.body[0], ast.If):
            return node

        new_body = []

        #  берем самую верхнюю ноду условия
        if_node: ast.If = while_node.body[0]


        return node


