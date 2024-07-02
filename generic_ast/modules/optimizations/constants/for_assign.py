from generic_ast.modules.optimizations.base import BaseTransformer
import ast_comments as ast
import operator


class For_Assign(BaseTransformer):
    def visit_For(self, node: ast.For):
        '''
            For(
                target=Name(id='目山鸟水子女月山人山马月鸟山目水', ctx=Store()),
                iter=Name(id='鸟口目水子口山日口日日鸟马月鸟水', ctx=Load()),
                body=[
                For(
                    target=Tuple(
                    elts=[
                        Name(id='子山日马女马人子馬鸟口山日马水馬', ctx=Store()),
                        Name(id='水日目鳥马目鳥口水木水人马日水子', ctx=Store()),
                        Name(id='鳥目马女女馬木月子刀子刀日木山刀', ctx=Store())],
                    ctx=Store())
        '''
        if node.target:
            if isinstance(node.target, ast.Name):
                var_name = node.target.id
                var_value = node.iter
                var_name = self.variable_generator(var_name, var_value)
                self.variables[var_name] = var_value
                node.target.id = var_name
            elif isinstance(node.target, ast.Tuple):
                for i, target in enumerate(node.target.elts):
                    if isinstance(target, ast.Name):
                        var_name = target.id
                        var_value = node.iter
                        var_name = self.variable_generator(var_name, var_value)
                        self.variables[var_name] = var_value
                        node.target.elts[i].id = var_name
        return node