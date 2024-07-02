from generic_ast.modules.optimizations.base import BaseTransformer
import builtins
import ast_comments as ast


class String_Asign(BaseTransformer):
    def visit_Assign(self, node: ast.Assign):
        '''
            Assign(
                targets=[
                    Name(id='YXKAthmSTyUldIpxcCbOeDrNauFVJLgRjvMznQEWPiwHBfkoGq', ctx=Store())],
                value=Constant(value='w5-DHKuAVn6WqR1C5P0aZYndaHjTdCMKnGdWNYeqzfE=')),
        '''
        if node.targets:
            for target in node.targets:
                if isinstance(target, ast.Name):
                    var_name = target.id
                    var_value = node.value
                    var_name = self.variable_generator(var_name, var_value)
                    self.variables[var_name] = var_value
                    target.id = var_name

        return node     